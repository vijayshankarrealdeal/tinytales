import asyncio
import numpy as np
from sklearn.cluster import KMeans
from pydantic import BaseModel
from typing import List

from engine.pallet_generator import (
    get_brightness,
    get_hue,
    get_saturation,
    open_image,
    rgb_to_hex,
)


class StoryPayloadIn(BaseModel):
    content: str
    image: str


class PayloadBaseIn(BaseModel):
    title: str
    poster: str
    chapters: List[StoryPayloadIn]


class PalletPayload(BaseModel):
    predominant: str
    dark: str
    light: str
    median_brightness: str
    most_saturated: str
    least_saturated: str
    coolest: str
    warmest: str

    @classmethod
    async def from_image(cls, image_path: str):
        # Offload the blocking image open and processing to a separate thread
        image = await asyncio.to_thread(open_image, image_path)
        # Resize the image for quicker processing
        image = image.resize((200, 200))
        # Convert image to a NumPy array and reshape to a set of RGB pixels
        image_np = np.array(image).reshape(-1, 3)

        # Run KMeans clustering (blocking call) in a thread
        kmeans = await asyncio.to_thread(KMeans, n_clusters=6, n_init=10)
        kmeans = await asyncio.to_thread(lambda: kmeans.fit(image_np))
        colors = kmeans.cluster_centers_.astype(int)

        labels = kmeans.labels_
        counts = np.bincount(labels)
        predominant = colors[np.argmax(counts)]

        brightness_sorted = sorted(colors, key=get_brightness)
        dark = brightness_sorted[0]
        light = brightness_sorted[-1]
        median_brightness = brightness_sorted[len(brightness_sorted) // 2]

        saturation_sorted = sorted(colors, key=get_saturation)
        most_saturated = saturation_sorted[-1]
        least_saturated = saturation_sorted[0]

        hue_sorted = sorted(colors, key=get_hue)
        coolest = hue_sorted[0]
        warmest = hue_sorted[-1]

        return cls(
            predominant=rgb_to_hex(predominant),
            dark=rgb_to_hex(dark),
            light=rgb_to_hex(light),
            median_brightness=rgb_to_hex(median_brightness),
            most_saturated=rgb_to_hex(most_saturated),
            least_saturated=rgb_to_hex(least_saturated),
            coolest=rgb_to_hex(coolest),
            warmest=rgb_to_hex(warmest),
        )


class StoryPayload(StoryPayloadIn):
    image_pallet: PalletPayload

    @classmethod
    async def create(cls, content: str, image_path: str):
        palette = await PalletPayload.from_image(image_path)
        return cls(content=content, image=image_path, image_pallet=palette)


class PayloadBaseOut(BaseModel):
    title: str
    poster: str
    poster_pallet: PalletPayload
    chapters: List[StoryPayload]

    @classmethod
    async def create(cls, data: PayloadBaseIn):
        poster_path = data.poster
        stories = data.chapters

        # Process poster and story images concurrently.
        poster_task = asyncio.create_task(PalletPayload.from_image(poster_path))
        story_tasks = [
            asyncio.create_task(
                StoryPayload.create(content=s.content, image_path=s.image)
            )
            for s in stories
        ]
        poster_palette, story_objs = await asyncio.gather(
            poster_task, asyncio.gather(*story_tasks)
        )
        return cls(
            title=data.title,
            poster=poster_path,
            poster_pallet=poster_palette,
            chapters=story_objs,
        )
