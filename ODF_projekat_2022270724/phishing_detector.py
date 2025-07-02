import pandas as pd
import re

#Učitavanje .csv fajla
df = pd.read_csv("mail_dataset.csv", encoding='latin-1', usecols=['label', 'text'])

#Definisanje phishing fraza i sumnjivih linkova
phishing_keywords = [
    'verify your account', 'update your information', 'account will be closed',
    'confirm your identity', 'urgent', 'action required', 'login now', 'click here',
    'security alert', 'your password', 'banking information', 'confirm billing',
    'restricted access', 'suspend', 'locked account', 'unauthorized access'
]

suspicious_link_patterns = [
    r'http[s]?://(?!www\.|secure\.|mail\.|accounts\.).*',
    r'\.ru', r'\.cn', r'\.tk', r'\.ml', r'\.ga',
    r'bit\.ly', r'tinyurl\.com'
]

#Heuristički pristup detekciji phishinf mejla
def is_phishing(text):
    text_lower = text.lower()
    score = 0

    for phrase in phishing_keywords:
        if phrase in text_lower:
            score += 1

    links = re.findall(r"http[s]?://\S+", text_lower)
    for link in links:
        for pattern in suspicious_link_patterns:
            if re.search(pattern, link):
                score += 1

    if any(term in text_lower for term in ['ssn', 'credit card', 'password']):
        score += 1

    return score >= 2

ham_emails = df[df['label'] == 'ham']
spam_emails = df[df['label'] == 'spam']
phishing_emails = df[df['text'].apply(is_phishing)]

#Prikaz broja mejlova po tipu
print("\n BROJ MEJLOVA U DATASETU")
print(f"Regularnih (HAM): {len(ham_emails)}")
print(f"Spam:              {len(spam_emails)}")
print(f"Phishing:          {len(phishing_emails)}")

#Izbor korisnika za prikaz mejlova
print("\n Opcije prikaza:")
print("1 - Prikaži REGULARNE mejlove")
print("2 - Prikaži SPAM mejlove")
print("3 - Prikaži PHISHING mejlove")
izbor = input("Unesite opciju (1/2/3): ")

#Prikaz odabranih mejlova (trenutno prikazuje samo jedan)
def prikazi_mejlove(dataframe, naziv):
    print(f"\n Prikazujem {len(dataframe)} {naziv.lower()} mejl:\n")
    for idx, row in dataframe.head(1).iterrows():
        print(f"! Index {idx} | Label: {row['label'].upper()}")
        print(row['text'])
        print("-" * 60)

if izbor == "1":
    prikazi_mejlove(ham_emails, "REGULARNIH")
elif izbor == "2":
    prikazi_mejlove(spam_emails, "SPAM")
elif izbor == "3":
    prikazi_mejlove(phishing_emails, "PHISHING")
else:
    print("Nevažeća opcija.")
