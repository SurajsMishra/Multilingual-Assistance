def classify_grievance(text: str):
    text_lower = text.lower()
    if(
        "water" in text_lower or "पानी" in text_lower
    ):
        return {
            "category": "Water Supply",
            "department": "Public Works",
            "priority": "high",
            "summary": "Water supply related complain"
        }
    elif(
        "road" in text_lower or "सड़क" in text_lower
    ):
        return{
            "category": "Roads & Infrastructure",
            "department": "Public Works",
            "priority": "medium",
            "summary": "Road related complaint"
        }
    elif(
        "electricity" in text_lower or "बिजली" in text_lower
    ):
        return{
            "category": "Electricity Supply",
            "department": "Energy Department",
            "priority": "medium",
            "summary": "Electricity supply related complaint"
        }
    elif(
        "waste" in text_lower or "कचरा" in text_lower
    ):
        return{
            "category": "Solid Waste Management",
            "department": "Municipal Corporation",
            "priority": "high",
            "summary": "Solid Waste Management related complaint"
        }
    elif(
        "ration" in text_lower or "राशन" in text_lower
    ):
        return{
            "category": "Food and Civil Supplies",
            "department": "Public Distribution System",
            "priority": "high",
            "summary": "Food and Civil Supplies related complaint"
        }
    else:
        return{
            "category": "General Public Service",
            "department": "Public Services",
            "priority": "low",
            "summary": "General service complaint"
        }