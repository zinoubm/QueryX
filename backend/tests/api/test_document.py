from httpx import AsyncClient

from app.core.config import settings
from app.models.user import User
from tests.utils import get_jwt_header
from tests.parser.data import dummy_pdf


class TestUpload:
    async def test_upload(
        self,
        client: AsyncClient,
        create_user,
    ):
        user: User = await create_user()
        jwt_header = get_jwt_header(user)

        pdf_path = dummy_pdf(dummy_text, temp_file_path="/tmp/temp_file_test.pdf")

        files = {"file": open(pdf_path, "rb")}

        resp = await client.post(
            settings.API_PATH + "/documents/upsert-file",
            headers=jwt_header,
            files=files,
        )

        assert resp.status_code == 200


# class TestUnsupportedUpload:
#     async def test_upload(
#         self,
#         client: AsyncClient,
#         create_user,
#     ):
#         user: User = await create_user()
#         jwt_header = get_jwt_header(user)

#         pdf_path = dummy_pdf(dummy_text, temp_file_path="/tmp/temp_file_test")

#         files = {"file": open(pdf_path, "rb")}

#         resp = await client.post(
#             settings.API_PATH + "/documents/upsert-file",
#             headers=jwt_header,
#             files=files,
#         )

#         assert resp.status_code == 200


dummy_text = """
Once upon a time, in a small village nestled deep within a lush green valley, there lived a young girl named Lily. She was known for her enchanting beauty, her sparkling blue eyes, and her heart full of kindness. Lily was an orphan, raised by the villagers who loved her as their own.

The village, called Meadowbrook, was a peaceful place where the sounds of laughter and joy filled the air. It was surrounded by fields of blooming flowers, where butterflies danced and birds sang their melodious tunes. Life was simple and harmonious in Meadowbrook.

Lily had always felt a deep connection with nature. She would often wander through the meadows, feeling the soft grass beneath her bare feet and breathing in the sweet scent of wildflowers. One day, as she sat beneath a towering oak tree, a gentle breeze whispered in her ear.

"Lily," the breeze seemed to say, "your destiny awaits beyond the borders of this village. Seek the mystical Land of Dreams, and you shall find your purpose."

Intrigued and excited by the mysterious message, Lily knew she had to embark on a journey to discover her true path. She bid farewell to the villagers who had cared for her and set off on an adventure filled with wonder and uncertainty.

Her first stop was the ancient Wise Woman of the Woods, who was rumored to possess great wisdom. The wise woman welcomed Lily with open arms and listened intently to her story. After a long pause, she spoke, "To find the Land of Dreams, you must embark on a quest to collect four enchanted objects: the Golden Feather of Hope, the Silver Locket of Love, the Sapphire Tear of Wisdom, and the Diamond Key of Courage. Each of these objects will guide you closer to your destination."

With a grateful heart and newfound determination, Lily set off on her quest. Her first destination was the Misty Mountains, where the Golden Feather of Hope was said to reside. The journey was treacherous, but Lily pressed on, fueled by her unwavering spirit. She braved icy winds and treacherous cliffs until she reached a hidden cave at the mountain's peak.

Inside the cave, a magnificent golden eagle awaited her arrival. The eagle possessed the Golden Feather of Hope, and it spoke in a voice filled with wisdom, "You have shown great courage and determination, young Lily. Take this feather, and let it guide you through the darkest of times."

Lily carefully took the feather, feeling its warmth and power in her hands. She thanked the golden eagle and continued her journey, now with a renewed sense of hope.

Next, she traveled to the Enchanted Forest, where the Silver Locket of Love was rumored to be hidden. The forest was a magical place, filled with talking animals and mystical creatures. With the help of a wise old owl named Oliver, Lily navigated through the dense foliage and arrived at a hidden grove.

In the grove, a majestic unicorn awaited her arrival. The unicorn gently placed the Silver Locket of Love around Lily's neck, saying, "Love is the key that unlocks the true potential within us all. Let this locket remind you of the power of love, and may it guide you on your journey."

Grateful for the unicorn's gift, Lily continued her quest with the locket close to her heart.

Her third destination was the Crystal Caverns, a breathtaking underground realm said to hold the Sapphire Tear of Wisdom. The caverns were filled with dazzling crystals that illuminated the path ahead, leading Lily deeper into the heart of the earth.

Finally, she reached a crystal-clear pool where a wise mermaid awaited her arrival. The mermaid held the Sapphire Tear of Wisdom in her hands and spoke in a melodious voice, "Wisdom comes from within, dear Lily. Take this tear and let it guide you to make wise choices on your journey."

Lily accepted the tear with gratitude, feeling a sense of enlightenment washing over her. With the Sapphire Tear of Wisdom in her possession, she felt more prepared than ever to face the challenges ahead.

The last leg of Lily's journey led her to the Forbidden Fortress, a formidable castle guarded by fierce creatures and dark magic. It was here that she was to find the Diamond Key of Courage. Lily summoned all her inner strength and faced her fears head-on, defeating the guardians and navigating the labyrinthine halls of the fortress.

Finally, she stood before the ancient Dragon of Courage, who possessed the key. The dragon's fiery breath and piercing gaze did not intimidate Lily. With a steady voice, she spoke, "I seek the Diamond Key of Courage to unlock my true destiny."

Impressed by her bravery, the dragon nodded and handed her the diamond key, saying, "You have proven yourself worthy, young one. May this key unlock the door to your greatest purpose."

Armed with the Golden Feather of Hope, the Silver Locket of Love, the Sapphire Tear of Wisdom, and the Diamond Key of Courage, Lily returned to Meadowbrook, her heart filled with anticipation. She knew that her journey had been more than just a quest for magical objects; it had been a journey of self-discovery and growth.

As Lily entered the village, the sky above her began to shimmer and sparkle. A magnificent rainbow appeared, stretching across the horizon. Following its vibrant colors, Lily walked toward a previously unseen path, and as she stepped onto it, the landscape transformed.

She found herself standing on the outskirts of a mystical land, the Land of Dreams. The air was filled with magic, and the beauty of the place left Lily breathless. She had arrived at her destination.

In the Land of Dreams, Lily discovered her true purpose—to bring hope, love, wisdom, and courage to those in need. With her magical objects, she traveled far and wide, touching the lives of countless individuals, helping them find their own paths and unlocking the magic within them.

Lily's journey continued for many years, as she embraced her role as a guardian of the Land of Dreams. Her love and compassion spread like ripples in a pond, inspiring others to follow their dreams and make a difference in the world.

And so, the young orphan girl named Lily became a legend, a symbol of hope and a testament to the transformative power of love, wisdom, and courage. Her story would be told for generations to come, reminding people of the magic that lies within us all.

"""

# class TestQuery:
#     async def test_query(
#         self,
#         client: AsyncClient,
#         create_user,
#     ):
#         user: User = await create_user()
#         jwt_header = get_jwt_header(user)
#         payload = {
#             "query": "What is the meaning of life?",
#             "document_id": "example.txt",
#         }
#         resp = await client.post(
#             settings.API_PATH + "/queries/",
#             json=payload,
#             headers=jwt_header,
#         )
#         assert resp.status_code == 200
