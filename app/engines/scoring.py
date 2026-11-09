def evaluate_candidate_skills(
        required_skills: list[str],
        extracted_skills: list[str]
) -> tuple[list[str],list[str], float]:
    """
    Deterministically evaluates match percentage between required and extracted skills
    using normalized case-insensitive substring matching.
    """
    if not required_skills:
        return [], [], 0.0
    matched_skills = []
    missing_skills = []
    
    extracted_normalized = [skill.strip().lower() for skill in extracted_skills]

    for req_skill in required_skills:
        clean_req = req_skill.strip().lower()
        if not clean_req:
            continue

        is_matched = any(
            clean_req == ext or clean_req in ext or ext in clean_req
            for ext in extracted_normalized
        )

        if is_matched:
            matched_skills.append(req_skill.strip())
        else:
            missing_skills.append(req_skill.strip())

    score = (len(matched_skills)/len(required_skills))*100.0

    return matched_skills, missing_skills, round(score,2)

