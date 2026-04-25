#!/usr/bin/env python3
"""
Day 1: Add 20 critical IPC sections
Focus: Kidnapping, Extortion, Robbery, Dacoity
"""

import json
from pathlib import Path

# Load existing sections
sections_file = Path("data/manual_sections/ipc_critical_sections.json")
with open(sections_file) as f:
    sections = json.load(f)

print(f"Current sections: {len(sections)}")

# Add 20 new sections
new_sections = [
    {
        "section_number": "363",
        "section_title": "Punishment for kidnapping",
        "content": "Whoever kidnaps any person from India or from lawful guardianship, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "offense_type": "kidnapping",
        "punishment_severity": "medium",
        "maximum_punishment_years": 7,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["kidnapping", "abduction", "lawful guardianship"]
    },
    {
        "section_number": "364",
        "section_title": "Kidnapping or abducting in order to murder",
        "content": "Whoever kidnaps or abducts any person in order that such person may be murdered or may be so disposed of as to be put in danger of being murdered, shall be punished with imprisonment for life or rigorous imprisonment for a term which may extend to ten years, and shall also be liable to fine.",
        "offense_type": "kidnapping",
        "punishment_severity": "severe",
        "maximum_punishment_years": 999,
        "minimum_punishment_years": 10,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["kidnapping", "abduction", "murder", "danger"]
    },
    {
        "section_number": "365",
        "section_title": "Kidnapping or abducting with intent secretly and wrongfully to confine person",
        "content": "Whoever kidnaps or abducts any person with intent to cause that person to be secretly and wrongfully confined, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "offense_type": "kidnapping",
        "punishment_severity": "medium",
        "maximum_punishment_years": 7,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["kidnapping", "abduction", "confinement", "wrongful"]
    },
    {
        "section_number": "366",
        "section_title": "Kidnapping, abducting or inducing woman to compel her marriage, etc.",
        "content": "Whoever kidnaps or abducts any woman with intent that she may be compelled, or knowing it to be likely that she will be compelled, to marry any person against her will, or in order that she may be forced or seduced to illicit intercourse, or knowing it to be likely that she will be forced or seduced to illicit intercourse, shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine.",
        "offense_type": "kidnapping",
        "punishment_severity": "high",
        "maximum_punishment_years": 10,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["kidnapping", "woman", "marriage", "forced", "seduction"]
    },
    {
        "section_number": "383",
        "section_title": "Extortion",
        "content": "Whoever intentionally puts any person in fear of any injury to that person, or to any other, and thereby dishonestly induces the person so put in fear to deliver to any person any property or valuable security, or anything signed or sealed which may be converted into a valuable security, commits 'extortion'.",
        "offense_type": "extortion",
        "punishment_severity": "medium",
        "maximum_punishment_years": 3,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["extortion", "fear", "threat", "property", "dishonest"]
    },
    {
        "section_number": "384",
        "section_title": "Punishment for extortion",
        "content": "Whoever commits extortion shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
        "offense_type": "extortion",
        "punishment_severity": "medium",
        "maximum_punishment_years": 3,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["extortion", "punishment"]
    },
    {
        "section_number": "385",
        "section_title": "Putting person in fear of injury in order to commit extortion",
        "content": "Whoever, in order to the committing of extortion, puts any person in fear, or attempts to put any person in fear, of any injury, shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both.",
        "offense_type": "extortion",
        "punishment_severity": "low",
        "maximum_punishment_years": 2,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["extortion", "fear", "threat", "injury"]
    },
    {
        "section_number": "390",
        "section_title": "Robbery",
        "content": "In all robbery there is either theft or extortion. When theft is robbery: Theft is 'robbery' if, in order to the committing of the theft, or in committing the theft, or in carrying away or attempting to carry away property obtained by the theft, the offender, for that end, voluntarily causes or attempts to cause to any person death or hurt or wrongful restraint, or fear of instant death or of instant hurt, or of instant wrongful restraint. When extortion is robbery: Extortion is 'robbery' if the offender, at the time of committing the extortion, is in the presence of the person put in fear, and commits the extortion by putting that person in fear of instant death, of instant hurt, or of instant wrongful restraint to that person or to some other person, and, by so putting in fear, induces the person so put in fear then and there to deliver up the thing extorted.",
        "offense_type": "robbery",
        "punishment_severity": "high",
        "maximum_punishment_years": 10,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["robbery", "theft", "extortion", "violence", "fear"]
    },
    {
        "section_number": "392",
        "section_title": "Punishment for robbery",
        "content": "Whoever commits robbery shall be punished with rigorous imprisonment for a term which may extend to ten years, and shall also be liable to fine; and, if the robbery be committed on the highway between sunset and sunrise, the imprisonment may be extended to fourteen years.",
        "offense_type": "robbery",
        "punishment_severity": "high",
        "maximum_punishment_years": 14,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["robbery", "punishment", "highway", "rigorous"]
    },
    {
        "section_number": "395",
        "section_title": "Punishment for dacoity",
        "content": "Whoever commits dacoity shall be punished with imprisonment for life, or with rigorous imprisonment for a term which may extend to ten years, and shall also be liable to fine.",
        "offense_type": "dacoity",
        "punishment_severity": "severe",
        "maximum_punishment_years": 999,
        "minimum_punishment_years": 10,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["dacoity", "gang robbery", "punishment"]
    },
    {
        "section_number": "396",
        "section_title": "Dacoity with murder",
        "content": "If any one of five or more persons, who are conjointly committing dacoity, commits murder in so committing dacoity, every one of those persons shall be punished with death, or imprisonment for life, or rigorous imprisonment for a term which may extend to ten years, and shall also be liable to fine.",
        "offense_type": "dacoity",
        "punishment_severity": "severe",
        "maximum_punishment_years": 1000,
        "minimum_punishment_years": 10,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["dacoity", "murder", "gang", "death penalty"]
    },
    {
        "section_number": "463",
        "section_title": "Forgery",
        "content": "Whoever makes any false document or false electronic record or part of a document or electronic record, with intent to cause damage or injury, to the public or to any person, or to support any claim or title, or to cause any person to part with property, or to enter into any express or implied contract, or with intent to commit fraud or that fraud may be committed, commits forgery.",
        "offense_type": "forgery",
        "punishment_severity": "medium",
        "maximum_punishment_years": 2,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["forgery", "false document", "fraud", "electronic record"]
    },
    {
        "section_number": "465",
        "section_title": "Punishment for forgery",
        "content": "Whoever commits forgery shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both.",
        "offense_type": "forgery",
        "punishment_severity": "low",
        "maximum_punishment_years": 2,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["forgery", "punishment"]
    },
    {
        "section_number": "468",
        "section_title": "Forgery for purpose of cheating",
        "content": "Whoever commits forgery, intending that the document or electronic record forged shall be used for the purpose of cheating, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "offense_type": "forgery",
        "punishment_severity": "medium",
        "maximum_punishment_years": 7,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["forgery", "cheating", "fraud", "document"]
    },
    {
        "section_number": "471",
        "section_title": "Using as genuine a forged document or electronic record",
        "content": "Whoever fraudulently or dishonestly uses as genuine any document or electronic record which he knows or has reason to believe to be a forged document or electronic record, shall be punished in the same manner as if he had forged such document or electronic record.",
        "offense_type": "forgery",
        "punishment_severity": "medium",
        "maximum_punishment_years": 7,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["forgery", "forged document", "fraudulent", "dishonest"]
    },
    {
        "section_number": "441",
        "section_title": "Criminal trespass",
        "content": "Whoever enters into or upon property in the possession of another with intent to commit an offence or to intimidate, insult or annoy any person in possession of such property, or having lawfully entered into or upon such property, unlawfully remains there with intent thereby to intimidate, insult or annoy any such person, or with intent to commit an offence, is said to commit 'criminal trespass'.",
        "offense_type": "trespass",
        "punishment_severity": "low",
        "maximum_punishment_years": 3,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["trespass", "property", "unlawful entry", "intimidate"]
    },
    {
        "section_number": "447",
        "section_title": "Punishment for criminal trespass",
        "content": "Whoever commits criminal trespass shall be punished with imprisonment of either description for a term which may extend to three months, or with fine which may extend to five hundred rupees, or with both.",
        "offense_type": "trespass",
        "punishment_severity": "low",
        "maximum_punishment_years": 0.25,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["trespass", "punishment"]
    },
    {
        "section_number": "448",
        "section_title": "Punishment for house-trespass",
        "content": "Whoever commits house-trespass shall be punished with imprisonment of either description for a term which may extend to one year, or with fine which may extend to one thousand rupees, or with both.",
        "offense_type": "trespass",
        "punishment_severity": "low",
        "maximum_punishment_years": 1,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": True,
        "cognizable": False,
        "keywords": ["house trespass", "dwelling", "punishment"]
    },
    {
        "section_number": "451",
        "section_title": "House-trespass in order to commit offence punishable with imprisonment",
        "content": "Whoever commits house-trespass in order to the committing of any offence punishable with imprisonment, shall be punished with imprisonment of either description for a term which may extend to two years, and shall also be liable to fine; and if the offence intended to be committed is theft, the term of the imprisonment may be extended to seven years.",
        "offense_type": "trespass",
        "punishment_severity": "medium",
        "maximum_punishment_years": 7,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["house trespass", "theft", "burglary", "offence"]
    },
    {
        "section_number": "452",
        "section_title": "House-trespass after preparation for hurt, assault or wrongful restraint",
        "content": "Whoever commits house-trespass, having made preparation for causing hurt to any person or for assaulting any person, or for wrongfully restraining any person, or for putting any person in fear of hurt, or of assault, or of wrongful restraint, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "offense_type": "trespass",
        "punishment_severity": "medium",
        "maximum_punishment_years": 7,
        "minimum_punishment_years": 0,
        "involves_imprisonment": True,
        "involves_fine": True,
        "bailable": False,
        "cognizable": True,
        "keywords": ["house trespass", "assault", "hurt", "restraint"]
    }
]

# Add to existing sections
sections.extend(new_sections)

# Save updated file
with open(sections_file, 'w') as f:
    json.dump(sections, f, indent=2, ensure_ascii=False)

print(f"Added {len(new_sections)} new sections")
print(f"Total sections now: {len(sections)}")
print("\nNew sections added:")
for sec in new_sections:
    print(f"  - {sec['section_number']}: {sec['section_title'][:60]}...")

print("\n✓ Day 1 complete! Run build_manual_db.py to rebuild database.")
