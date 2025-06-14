import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

ml_phrases = ["Machine Learning","ML", "ML Models", "Regression", "Classification", "clustering", "NLP", "predictions"]
ml_patterns = [nlp.make_doc(text) for text in ml_phrases]
matcher.add("ML_TASK", ml_patterns)

dashboard_phrases = ["dashboard", "analytics panel", "admin interface", "visual report", "data dashboard"]
dashboard_patterns = [nlp.make_doc(text) for text in dashboard_phrases]
matcher.add("DASHBOARD", dashboard_patterns)

realtime_phrases = ["real-time", "live updates", "instant feedback", "streaming data", "fast response"]
realtime_patterns = [nlp.make_doc(text) for text in realtime_phrases]
matcher.add("REALTIME", realtime_patterns)

webapp_phrases = ["web app", "online tool", "browser-based", "responsive web", "single-page app"]
webapp_patterns = [nlp.make_doc(text) for text in webapp_phrases]
matcher.add("WEB_APP", webapp_patterns)

mobile_phrases = ['mobile app', 'android', 'ios', 'phone', 'mobile application', 'mobile']
mobile_patterns = [nlp.make_doc(text) for text in mobile_phrases]
matcher.add("MOBILE_APP", mobile_patterns)

def get_recommendations(description):
    doc = nlp(description)
    matches = matcher(doc)
    
    matched_labels = set(nlp.vocab.strings[match_id] for match_id, _, _ in matches)

    # Basic rule-based mapping
    recommendations = {}
    reasoning = {}

    if "MOBILE_APP" in matched_labels:
        recommendations["frontend"] = "React Native"
        recommendations["backend"] = "FastAPI"
        recommendations["database"] = "SQLite"
        reasoning["frontend"] = "React Native is ideal for cross-platform mobile development."
        reasoning["backend"] = "FastAPI offers high performance for mobile APIs."

    if "WEB_APP" in matched_labels:
        recommendations["frontend"] = "React"
        recommendations["backend"] = "FastAPI"
        recommendations["database"] = "PostgreSQL"
        reasoning["frontend"] = "React is fast and widely used for web interfaces."
        reasoning["backend"] = "FastAPI is lightweight and ideal for APIs."

    if "ML_TASK" in matched_labels:
        recommendations["ml"] = "scikit-learn"
        reasoning["ml"] = "scikit-learn is a great starting point for ML projects."

    return {
        "recommended_stack": recommendations,
        "why_this_stack": reasoning
    }


