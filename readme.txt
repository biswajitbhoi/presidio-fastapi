python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt


uvicorn app.main:app --reload


-----------------------
http://127.0.0.1:8000/anonymize/

Request->

{
  "text": "Here are a few example sentences we currently support:\n\nHi, my name is David Johnson and I'm originally from Liverpool.\nMy credit card number is 4095-2609-9393-4932 and my crypto wallet id is 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ.\n\nOn 11/10/2024 I visited www.microsoft.com and sent an email to test@presidio.site, from IP 192.168.0.1.\n\nMy passport: 191280342 and my phone number: (212) 555-1234.\n\nThis is a valid International Bank Account Number: IL150120690000003111111 . Can you please check the status on bank account 954567876544?\n\nKate's social security number is 078-05-1126. Her driver license? it is 1234567A.",
  "entities": ["PERSON", "PHONE_NUMBER","EMAIL_ADDRESS","URL","US_BANK_NUMBER"],
  "language": "en"
}

Response->

{
    "anonymized_text": {
        "text": "Here are a few example sentences we currently support:\n\nHi, my name is <PERSON> and I'm originally from Liverpool.\nMy credit card number is 4095-2609-9393-4932 and my crypto wallet id is 16Yeky6GMjeNkAiNcBY7ZhrLoMSgg1BoyZ.\n\nOn 11/10/2024 I visited <URL> and sent an email to <EMAIL_ADDRESS>, from IP 192.168.0.1.\n\nMy passport: <US_BANK_NUMBER> and my phone number: <PHONE_NUMBER>.\n\nThis is a valid International Bank Account Number: IL150120690000003111111 . Can you please check the status on bank account <US_BANK_NUMBER>?\n\n<PERSON>'s social security number is <PHONE_NUMBER>. Her driver license? it is 1234567A.",
        "items": [
            {
                "start": 563,
                "end": 577,
                "entity_type": "PHONE_NUMBER",
                "text": "<PHONE_NUMBER>",
                "operator": "replace"
            },
            {
                "start": 526,
                "end": 534,
                "entity_type": "PERSON",
                "text": "<PERSON>",
                "operator": "replace"
            },
            {
                "start": 507,
                "end": 523,
                "entity_type": "US_BANK_NUMBER",
                "text": "<US_BANK_NUMBER>",
                "operator": "replace"
            },
            {
                "start": 365,
                "end": 379,
                "entity_type": "PHONE_NUMBER",
                "text": "<PHONE_NUMBER>",
                "operator": "replace"
            },
            {
                "start": 327,
                "end": 343,
                "entity_type": "US_BANK_NUMBER",
                "text": "<US_BANK_NUMBER>",
                "operator": "replace"
            },
            {
                "start": 275,
                "end": 290,
                "entity_type": "EMAIL_ADDRESS",
                "text": "<EMAIL_ADDRESS>",
                "operator": "replace"
            },
            {
                "start": 248,
                "end": 253,
                "entity_type": "URL",
                "text": "<URL>",
                "operator": "replace"
            },
            {
                "start": 71,
                "end": 79,
                "entity_type": "PERSON",
                "text": "<PERSON>",
                "operator": "replace"
            }
        ]
    }
}