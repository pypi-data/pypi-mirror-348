from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Sequence, Dict, Any

import PIL.Image
import gymnasium as gym
import numpy as np
from PIL import Image, ImageDraw
from PIL.Image import Resampling
from scipy.interpolate import RegularGridInterpolator

from ap_gym import ImageSpace
from ap_gym.envs.dataset import BufferedIterator, DataLoader, DatasetBatchIterator
from ap_gym.envs.style import COLOR_AGENT, quality_color
from .image_classification_dataset import ImageClassificationDataset


@dataclass(frozen=True)
class ImagePerceptionConfig:
    dataset: ImageClassificationDataset
    sensor_size: tuple[int, int] = (5, 5)
    sensor_scale: float = 1.0
    max_step_length: float | Sequence[float] = 0.2
    step_limit: int = 16
    display_visitation: bool = True
    render_unvisited_opacity: float = 0.0
    render_visited_opacity: float = 0.3
    prefetch_buffer_size: int = 128
    prefetch: bool = True


ObsType = dict[Literal["glimpse", "glimpse_pos", "time_step"], np.ndarray]


class ImagePerceptionModule:
    def __init__(
        self,
        num_envs,
        config: ImagePerceptionConfig,
    ):
        self.__config = config
        self.__num_envs = num_envs
        # Target position of the sensor relative to the previous position of the sensor
        self.__single_inner_action_space = gym.spaces.Box(
            -np.ones(2, dtype=np.float32), np.ones(2, dtype=np.float32)
        )
        self.__current_data_point_idx: int | None = None
        self.__current_images: np.ndarray | None = None
        self.__interpolated_images: list[RegularGridInterpolator] | None = None
        self.__terminating = None
        self.__config.dataset.load()
        *self.__image_size, self.__channels = self.__config.dataset[0][0].shape
        self.__observation_space_dict = {
            "glimpse": ImageSpace(
                self.__config.sensor_size[1],
                self.__config.sensor_size[0],
                self.__channels,
                dtype=np.float32,
            ),
            "glimpse_pos": gym.spaces.Box(-1, 1, (2,), np.float32),
            "time_step": gym.spaces.Box(-1, 1, (), np.float32),
        }
        self.__current_sensor_pos_norm: np.ndarray | None = None
        self.__current_time_step = None
        max_step_length = np.array(self.__config.max_step_length)
        assert max_step_length.shape in {(2,), (1,), ()}
        self.__max_step_length = np.ones(2) * np.array(max_step_length)
        self.__current_rng = None
        self.__render_size = self.__render_scaling = None
        self.__visitation_counts = self.__prediction_quality_map = None
        self.__prev_done: np.ndarray | None = None
        self.__current_labels: np.ndarray | None = None
        self.__data_loader: DataLoader | None = None

    def seed(self, seed: int | None = None):
        self.__current_rng = np.random.default_rng(seed)
        if self.__data_loader is not None:
            self.__data_loader.close()
        iterator = DatasetBatchIterator(
            self.__config.dataset,
            batch_size=self.__num_envs,
            seed=self.__current_rng.integers(0, 2**32 - 1, endpoint=True),
        )
        self.__data_loader = DataLoader(
            iterator,
            prefetch=self.__config.prefetch,
            prefetch_buffer_size=self.__config.prefetch_buffer_size,
        )

    def reset(self) -> tuple[ObsType, dict[str, Any]]:
        if self.__current_rng is None:
            self.seed()
        (
            (
                self.__current_images,
                self.__current_labels,
            ),
            self.__current_data_point_idx,
        ) = next(self.__data_loader)
        image_size = np.array(self.__current_images.shape[1:3])
        if np.any(image_size < self.effective_sensor_size):
            raise ValueError(
                f"Image size {tuple(image_size)} cannot be smaller than effective sensor size "
                f"{tuple(self.effective_sensor_size)}."
            )
        coords_y = (
            np.arange(0, self.__current_images.shape[1])
            - (self.__current_images.shape[1] - 1) / 2
        )
        coords_x = (
            np.arange(0, self.__current_images.shape[2])
            - (self.__current_images.shape[2] - 1) / 2
        )
        self.__interpolated_images = [
            RegularGridInterpolator((coords_y, coords_x), img, method="linear")
            for img in self.__current_images
        ]

        self.__current_sensor_pos_norm = self.__current_rng.uniform(
            -1, 1, size=(self.__num_envs, 2)
        )
        info = {"index": self.__current_data_point_idx}
        self.__current_time_step = 0

        obs = self._get_obs()

        if self.__visitation_counts is None:
            render_width = max(128, obs["glimpse"].shape[2])
            self.__render_scaling = render_width / self.__image_size[1]
            render_height = int(round(self.__render_scaling * self.__image_size[0]))
            self.__render_size = (render_width, render_height)
            self.__visitation_counts = np.zeros(
                (self.__num_envs, self.__render_size[1], self.__render_size[0]),
                dtype=np.int32,
            )
            self.__prediction_quality_map = np.zeros(
                (
                    self.__num_envs,
                    self.__render_size[1],
                    self.__render_size[0],
                ),
                dtype=np.float32,
            )
        else:
            self.__visitation_counts.fill(0)
            self.__prediction_quality_map.fill(0)

        self.__prev_done = np.zeros(self.__num_envs, dtype=np.bool_)
        return obs, info

    def step(
        self, action: np.ndarray, prediction_quality: np.ndarray
    ) -> tuple[ObsType, np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
        if np.any(np.isnan(prediction_quality)):
            raise ValueError("NaN values detected in prediction.")
        self.__update_visitation_overlay(prediction_quality=prediction_quality)
        if np.any(self.__prev_done):
            if not np.all(self.__prev_done):
                raise NotImplementedError("Partial reset is not supported.")
            obs, info = self.reset()
            terminated = False
            base_reward = np.zeros(self.__num_envs)
        else:
            action_clipped = np.clip(action, -1, 1)
            if np.any(np.isnan(action_clipped)):
                raise ValueError("NaN values detected in action.")
            step = self.__max_step_length * action_clipped
            new_sensor_pos_norm = self.__current_sensor_pos_norm + step
            self.__current_sensor_pos_norm = np.clip(new_sensor_pos_norm, -1, 1)
            base_reward = -np.linalg.norm(action, axis=-1) * 1e-3
            info = {"index": self.__current_data_point_idx}
            self.__current_time_step += 1
            terminated = self.__current_time_step >= self.__config.step_limit
            obs = self._get_obs()
        terminated_arr = np.full(self.__num_envs, terminated)
        truncated_arr = np.zeros(self.__num_envs, dtype=np.bool_)
        self.__prev_done = terminated_arr | truncated_arr
        return (obs, base_reward, terminated_arr, truncated_arr, info)

    def __update_visitation_overlay(self, prediction_quality: np.ndarray | None = None):
        pos, size = self.__sensor_rects
        pos = np.round(pos).astype(np.int32)
        size = np.round(np.flip(size)).astype(np.int32)
        x_range = pos[..., 0, None] + np.arange(size[0]) - size[0] // 2
        y_range = pos[..., 1, None] + np.arange(size[1]) - size[1] // 2
        coords = (
            np.arange(self.__num_envs)[:, None, None],
            np.clip(y_range, 0, self.__visitation_counts.shape[1] - 1)[:, :, None],
            np.clip(x_range, 0, self.__visitation_counts.shape[2] - 1)[:, None, :],
        )
        self.__visitation_counts[coords] += 1
        if prediction_quality is not None:
            self.__prediction_quality_map[coords] = np.clip(
                prediction_quality[:, None, None], 0, 1
            )

    def _get_obs(self) -> ObsType:
        return {
            "glimpse": self.get_glimpse(self.__current_sensor_pos_norm),
            "glimpse_pos": self.__current_sensor_pos_norm.astype(np.float32),
            "time_step": np.full(
                self.__num_envs,
                (self.__current_time_step / self.__config.step_limit) * 2 - 1,
                np.float32,
            ),
        }

    def get_glimpse(self, pos_norm: np.ndarray) -> np.ndarray:
        sensing_point_offsets = np.meshgrid(
            (
                np.arange(self.__config.sensor_size[0])
                - (self.__config.sensor_size[0] - 1) / 2
            )
            * self.__config.sensor_scale,
            (
                np.arange(self.__config.sensor_size[1])
                - (self.__config.sensor_size[1] - 1) / 2
            )
            * self.__config.sensor_scale,
            indexing="ij",
        )
        sensing_points = (
            np.flip(self.denormalize_coords(pos_norm), axis=-1)[:, None, None]
            + np.stack(sensing_point_offsets, axis=-1)[None]
        )
        return (
            np.stack(
                [
                    img(sp)
                    for img, sp in zip(self.__interpolated_images, sensing_points)
                ],
                axis=0,
            )
            .clip(0, 1)
            .astype(np.float32)
        )

    def render(
        self, return_pil_imgs: bool = False
    ) -> np.ndarray | list[PIL.Image.Image] | None:
        current_image = self.__current_images
        if self.__channels == 1:
            current_image = current_image[..., 0]
        elif self.__channels != 3:
            raise NotImplementedError()
        rgb_imgs = []
        pos, size = self.__sensor_rects
        top_left = pos - size / 2
        bottom_right = pos + size / 2

        glimpse_shadow_offset = self.glimpse_border_width

        visited = self.__visitation_counts > 0
        overlay = (
            (
                visited[..., None]
                * np.concatenate(
                    [
                        quality_color(self.__prediction_quality_map),
                        np.full_like(
                            self.__prediction_quality_map[..., None],
                            int(255 * self.__config.render_visited_opacity),
                        ),
                    ],
                    axis=-1,
                )
                + ~visited[..., None]
                * (0, 0, 0, int(255 * self.__config.render_unvisited_opacity))
            )
            .round()
            .astype(np.uint8)
        )
        for img, tl, br, ol in zip(current_image, top_left, bottom_right, overlay):
            rgb_img = (
                Image.fromarray((img * 255).astype(np.uint8))
                .resize(self.__render_size, resample=Resampling.NEAREST)
                .convert("RGB")
            )

            if self.__config.display_visitation:
                # Unfortunately, we cannot use Pillows alpha_composite here because it does not support RBG base images.
                # We cannot change the base image to RGBA because of a bug in Pillow that prevents the rectangle from
                # being drawn correctly. See: https://github.com/python-pillow/Pillow/issues/2496
                # So we do it manually here.
                alpha = ol[..., -1:] / 255
                rgb_img = Image.fromarray(
                    (np.array(rgb_img) * (1 - alpha) + alpha * ol[..., :-1]).astype(
                        np.uint8
                    )
                )

            draw = ImageDraw.Draw(rgb_img, "RGBA")
            glimpse_coords = np.concatenate([tl, br])
            draw.rectangle(
                tuple(glimpse_coords + glimpse_shadow_offset),
                outline=(0, 0, 0, 80),
                width=self.glimpse_border_width,
            )
            draw.rectangle(
                tuple(glimpse_coords),
                outline=COLOR_AGENT,
                width=self.glimpse_border_width,
            )
            rgb_imgs.append(rgb_img)

        return rgb_imgs if return_pil_imgs else np.asarray(rgb_imgs)

    def denormalize_coords(self, size: np.ndarray) -> np.ndarray:
        sensor_pos_lim = (
            np.flip(np.array(self.__current_images.shape[1:3])) - 1
        ) / 2 - (self.effective_sensor_size - 1) / 2
        return size * sensor_pos_lim

    def to_render_coords(self, pos_norm: np.ndarray) -> np.ndarray:
        return self.scale_to_render_coords(pos_norm) + np.array(self.__render_size) / 2

    def scale_to_render_coords(self, size_norm: np.ndarray) -> np.ndarray:
        return self.denormalize_coords(size_norm) * self.__render_scaling

    def close(self):
        if isinstance(self.__data_loader, BufferedIterator):
            self.__data_loader.close()

    @property
    def sensor_size(self) -> tuple[int, int]:
        return self.__config.sensor_size

    @property
    def image_size(self) -> tuple[int, int]:
        return self.__image_size

    @property
    def effective_sensor_size(self):
        return np.array(self.__config.sensor_size) * self.__config.sensor_scale

    @property
    def current_sensor_pos(self):
        return self.denormalize_coords(self.__current_sensor_pos_norm)

    @property
    def __sensor_rects(self):
        pos = self.to_render_coords(self.__current_sensor_pos_norm)
        size = self.effective_sensor_size * self.__render_scaling
        return pos, size

    @property
    def observation_space_dict(self) -> Dict[str, gym.spaces.Space]:
        return self.__observation_space_dict

    @property
    def single_inner_action_space(self) -> gym.spaces.Box:
        return self.__single_inner_action_space

    @property
    def config(self):
        return self.__config

    @property
    def current_images(self) -> np.ndarray:
        return self.__current_images

    @property
    def glimpse_border_width(self):
        return max(1, int(round(1 / 128 * self.__render_size[0])))

    @property
    def current_labels(self) -> np.ndarray:
        return self.__current_labels

    @property
    def render_scaling(self):
        return self.__render_scaling

    @property
    def render_size(self):
        return self.__render_size
