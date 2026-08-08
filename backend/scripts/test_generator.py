"""Test generator."""
import sys
sys.path.insert(0, r"D:\KrishokChat Advisory System\backend")

from app.services.advisory.generator import generate_response, build_prompt


def main():
    import traceback
    # Test 1: Category A disease (potato late blight) with full info
    print("=" * 60)
    print("Test 1: Potato Late Blight (Category A - full info)")
    try:
        result = generate_response(
            query="আলুর দেরি ব্লাইট রোগের প্রতিকার কি?",
            detected_crop="Potato",
            detected_disease="Late Blight",
            intent="treatment",
            retrieved_nodes=[
                {"id": "CABI_POTATO_834B4F_001", "title_en": "Potato Late Blight Management",
                 "content_bn": "আলুর দেরি ব্লাইট রোগ Phytophthora infestans ছত্রাকের কারণে হয়।"},
            ],
            disease_details={
                "description_bn": "পাতায় দূর্গন্ধযুক্ত দাগ দেখা দেয়।",
                "solution_bn": "প্রতি লিটার পানিতে ২ গ্রাম Mancozeff মিশিয়ে স্প্রে করুন।",
            },
        )
        print(f"Response: {result['response'][:300]}")
        print(f"Grounded: {result['grounded']}, Model: {result.get('model_used')}")
    except Exception as e:
        traceback.print_exc()
    print()

    # Test 2: Category C disease (no info in database)
    print("=" * 60)
    print("Test 2: Wheat Fusarium Foot Rot (Category C - no info)")
    result2 = generate_response(
        query="গমের ফিউজেরিয়াম ফুট রট দূর করতে কী কী করব?",
        detected_crop="Wheat",
        detected_disease="Fusarium Foot Rot",
        intent="treatment",
        retrieved_nodes=[],
        disease_details=None,
    )
    print(f"Response: {result2['response'][:300]}")
    print(f"Grounded: {result2['grounded']}, has_knowledge: {result2.get('has_knowledge')}")
    print()

    # Test 3: General question (no detection)
    print("=" * 60)
    print("Test 3: General agricultural question")
    result3 = generate_response(
        query="ধান কখন কাটতে হয়?",
        detected_crop="Rice",
        detected_disease=None,
        intent="general_info",
        retrieved_nodes=[
            {"id": "IRRI_IRRI_001", "title_en": "Rice Harvesting",
             "content_bn": "ধান ৮০-৮৫% পাকলে কাটতে হয়।"},
        ],
    )
    print(f"Response: {result3['response'][:300]}")
    print(f"Grounded: {result3['grounded']}")
    print()


if __name__ == "__main__":
    main()
