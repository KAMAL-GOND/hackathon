# code
import math

SKILL_ALIASES = {
    "python":"python","pyhton":"python","java":"java",
    "javascript":"javascript","javascrpit":"javascript","js":"javascript",
    "typescript":"typescript","typescrpit":"typescript",
    "c++":"cpp","cpp":"cpp","r":"r","kotlin":"kotlin",
    "machinelearning":"machine_learning","machine learning":"machine_learning",
    "ml":"machine_learning","sklearn":"machine_learning",
    "deeplearning":"deep_learning","deep learning":"deep_learning",
    "deep-learning":"deep_learning",
    "tensorflow":"tensorflow","pytorch":"pytorch","keras":"keras",
    "nlp":"nlp","bert":"bert","xgboost":"xgboost",
    "feature engineering":"feature_engineering",
    "statistics":"statistics","stats":"statistics",
    "regression":"regression","clustering":"clustering",
    "data-viz":"data_visualization","data visualization":"data_visualization",
    "data viz":"data_visualization","matplotlib":"data_visualization",
    "tableau":"data_visualization","power-bi":"data_visualization",
    "power bi":"data_visualization","powerbi":"data_visualization",
    "pandas":"pandas","numpy":"numpy",
    "react":"react","reacts":"react","reactjs":"react",
    "vue":"vue","vue.js":"vue","vuejs":"vue",
    "redux":"redux","tailwind":"tailwind",
    "html/css":"html_css","html css":"html_css","html":"html_css","css":"html_css",
    "jest":"jest","graphql":"graphql",
    "node.js":"nodejs","nodejs":"nodejs","node js":"nodejs",
    "flask":"flask","spring boot":"spring_boot","springboot":"spring_boot",
    "rest api":"rest_api","rest":"rest_api","restapi":"rest_api",
    "microservices":"microservices",
    "sql":"sql","mysql":"mysql","mysq":"mysql",
    "postgresql":"postgresql","postgres":"postgresql",
    "mongodb":"mongodb","redis":"redis","docker":"docker",
    "kubernetes":"kubernetes","kubernates":"kubernetes","k8s":"kubernetes",
    "ci/cd":"ci_cd","cicd":"ci_cd","ci cd":"ci_cd","aws":"aws",
    "android":"android","firebase":"firebase",
    "algorithms":"algorithms","algoritms":"algorithms",
    "data structure":"data_structures","data structures":"data_structures",
    "competitive programming":"competitive_programming",
    "ui/ux":"ui_ux","ui ux":"ui_ux","figma":"figma",
}

RESUMES = [
    ("01","Arjun Sharma","Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning"),
    ("02","Priya Nair","JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS"),
    ("03","Rahul Gupta","Java, Spring Boot, MySql, Microservices, Docker, kubernates"),
    ("04","Sneha Patel","Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib"),
    ("05","Vikram Singh","C++, Algoritms, Data Structure, competitive programming, python"),
    ("06","Ananya Krishnan","javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD"),
    ("07","Karan Mehta","Python, Sklearn, XGboost, feature engineering, SQL, tableau"),
    ("08","Deepika Rao","Java, Android, Kotlin, Firebase, REST, UI/UX, figma"),
    ("09","Aditya Kumar","Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest"),
    ("10","Meera Iyer","python, R, statistics, ML, regression, clustering, Power-BI"),
]

JDS = [
    ("JD-1","Kakao","ML Engineer",
     "python, machine learning, deep learning, tensorflow, pytorch, sql, data visualization, nlp, bert, feature engineering, statistics"),
    ("JD-2","Naver","Backend Engineer",
     "java, spring boot, mysql, postgresql, microservices, docker, kubernetes, rest api, ci/cd, redis"),
    ("JD-3","Line","Frontend Engineer",
     "javascript, react, vue, typescript, rest api, html/css, node.js, graphql, redux, jest, aws"),
]

MULTI_WORD = sorted([k for k in SKILL_ALIASES if " " in k], key=len, reverse=True)

def normalize(raw):
    tokens = [t.strip().lower() for t in raw.split(",")]
    result = []
    for token in tokens:
        matched = None
        for phrase in MULTI_WORD:
            if token == phrase:
                matched = SKILL_ALIASES[phrase]
                break
        if not matched and token in SKILL_ALIASES:
            matched = SKILL_ALIASES[token]
        if matched:
            result.append(matched)
    seen = set()
    deduped = []
    for s in result:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    return deduped

norm_resumes = []
for rid, name, raw in RESUMES:
    skills = normalize(raw)
    norm_resumes.append((rid, name, skills))

vocab = sorted(set(s for _,_,skills in norm_resumes for s in skills))

df = {term: sum(1 for _,_,skills in norm_resumes if term in skills) for term in vocab}
idf = {term: math.log(10 / df[term]) for term in vocab}

def tfidf_vector(skills):
    N = len(skills)
    return [(1/N * idf[term]) if term in skills else 0.0 for term in vocab]

resume_vectors = [(name, tfidf_vector(skills)) for _,name,skills in norm_resumes]

def jd_vector(raw):
    skills = normalize(raw)
    return [1 if term in skills else 0 for term in vocab]

def cosine(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    return dot/(na*nb) if na and nb else 0.0

for jd_id, company, role, jd_raw in JDS:
    jd_vec = jd_vector(jd_raw)
    scores = sorted([(n, cosine(rv, jd_vec)) for n,rv in resume_vectors],
                    key=lambda x: (-x[1], x[0]))
    print(f"\n{jd_id} — {company} ({role})")
    print(", ".join(f"{n}({s:.2f})" for n,s in scores[:3]))
