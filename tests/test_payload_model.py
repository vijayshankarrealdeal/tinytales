import pytest

from models.payload_base import PayloadBaseOut, PayloadBaseIn


def test_payload_input():
    payload = {
        "title": "Luna and the Starlight Adventure",
        "poster": "tests/11.jpg",
        "story": [
            {
                "content": "Luna was a curious little fox who lived in the whispering woods. She loved watching the stars every night from her cozy treehouse.",
                "image": "tests/11.jpg",
            },
        ],
    }
    payload_in = PayloadBaseIn(**payload)
    # Create and print the output
    t = PayloadBaseOut.create(payload_in)
    assert t.poster_pallet.dark == "05234f"

    payload = [
        {
            "title": "Luna and the Starlight Adbenture",
            "poster": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_poster.webp?",
            "poster_pallet": {
                "predominant": "365e61",
                "dark": "365e61",
                "light": "f6ead4",
                "median_brightness": "a3b8aa",
                "most_saturated": "f06333",
                "least_saturated": "a3b8aa",
                "coolest": "f06333",
                "warmest": "365e61",
            },
            "story": [
                {
                    "content": "Luna was a curious little fox who lived in the whispering woods. She loved watching the stars every night from her cozy treehouse.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_1.webp?",
                    "image_pallet": {
                        "predominant": "553332",
                        "dark": "553332",
                        "light": "e3ddc4",
                        "median_brightness": "8ea59e",
                        "most_saturated": "a86653",
                        "least_saturated": "e3ddc4",
                        "coolest": "553332",
                        "warmest": "597172",
                    },
                },
                {
                    "content": "One evening, Luna saw a star twinkle three times and then disappear. \u201cThat star needs help!\u201d she gasped.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_2.webp?",
                    "image_pallet": {
                        "predominant": "b57f6f",
                        "dark": "7e5632",
                        "light": "f9eccb",
                        "median_brightness": "c3a083",
                        "most_saturated": "7e5632",
                        "least_saturated": "f9eccb",
                        "coolest": "b57f6f",
                        "warmest": "888c6a",
                    },
                },
                {
                    "content": "With her tiny backpack and a glowing lantern, Luna set off on a nighttime adventure to find the missing star.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_3.webp?",
                    "image_pallet": {
                        "predominant": "736ea1",
                        "dark": "562b38",
                        "light": "e5cfd5",
                        "median_brightness": "c28e9f",
                        "most_saturated": "562b38",
                        "least_saturated": "e5cfd5",
                        "coolest": "8bb7db",
                        "warmest": "e5cfd5",
                    },
                },
                {
                    "content": "She met Hoot the Owl, who pointed to a shimmering path in the sky. \u201cFollow the glitter trail,\u201d he said wisely.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_4.webp?",
                    "image_pallet": {
                        "predominant": "415571",
                        "dark": "562242",
                        "light": "e9c6ad",
                        "median_brightness": "668b97",
                        "most_saturated": "562242",
                        "least_saturated": "9db3b3",
                        "coolest": "b45554",
                        "warmest": "562242",
                    },
                },
                {
                    "content": "Luna leapt from cloud to cloud, following the trail. She wasn\u2019t afraid\u2014her heart was full of wonder.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_5.webp?",
                    "image_pallet": {
                        "predominant": "e3c1b8",
                        "dark": "8a3c36",
                        "light": "faf5e2",
                        "median_brightness": "e79e72",
                        "most_saturated": "8a3c36",
                        "least_saturated": "faf5e2",
                        "coolest": "8a3c36",
                        "warmest": "a99bb2",
                    },
                },
                {
                    "content": "At last, she found the missing star caught in a spiderweb made of night. \u201cDon\u2019t worry, I\u2019ll free you,\u201d she whispered.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_6.webp?",
                    "image_pallet": {
                        "predominant": "a58690",
                        "dark": "792c2b",
                        "light": "f2e1b0",
                        "median_brightness": "7c97ac",
                        "most_saturated": "792c2b",
                        "least_saturated": "a58690",
                        "coolest": "792c2b",
                        "warmest": "a58690",
                    },
                },
                {
                    "content": "With care and kindness, Luna untangled the star. It sparkled brighter than ever before and danced in the sky.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_7.webp?",
                    "image_pallet": {
                        "predominant": "78829e",
                        "dark": "7e3050",
                        "light": "f3e3bc",
                        "median_brightness": "ae96a7",
                        "most_saturated": "7e3050",
                        "least_saturated": "ae96a7",
                        "coolest": "e1b2a0",
                        "warmest": "7e3050",
                    },
                },
                {
                    "content": "The star zipped back into its place. The sky twinkled with joy, and Luna felt proud.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_8.webp?",
                    "image_pallet": {
                        "predominant": "82a1a1",
                        "dark": "7c444d",
                        "light": "f2ead4",
                        "median_brightness": "b2b2b1",
                        "most_saturated": "ea806a",
                        "least_saturated": "b2b2b1",
                        "coolest": "ea806a",
                        "warmest": "7c444d",
                    },
                },
                {
                    "content": "When she returned home, the woods were glowing with soft starlight. Luna snuggled in bed, her heart full of magic.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_9.webp?",
                    "image_pallet": {
                        "predominant": "c0a19a",
                        "dark": "5c311b",
                        "light": "f0d8c7",
                        "median_brightness": "d2824b",
                        "most_saturated": "5c311b",
                        "least_saturated": "8d7979",
                        "coolest": "8d7979",
                        "warmest": "f0d8c7",
                    },
                },
                {
                    "content": "And from that night on, whenever a star blinked three times, Luna knew it was saying thank you.",
                    "image": "https://iqescxirvpvbjkifbrwu.supabase.co/storage/v1/object/public/childapps/images/s1_10.webp?",
                    "image_pallet": {
                        "predominant": "debfae",
                        "dark": "824037",
                        "light": "f5ecd7",
                        "median_brightness": "b39c9f",
                        "most_saturated": "824037",
                        "least_saturated": "f5ecd7",
                        "coolest": "bb766d",
                        "warmest": "b39c9f",
                    },
                },
            ],
        }
    ]

    t = PayloadBaseOut(**payload[0])
    assert t.poster_pallet.dark == "365e61"