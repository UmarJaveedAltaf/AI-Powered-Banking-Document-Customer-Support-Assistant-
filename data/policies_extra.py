"""Additional policies. Topics deliberately avoid the hallucination test subjects
(cryptocurrency, education loans, gold loans, fixed deposits, safe deposit lockers),
which must remain outside the corpus so the refusal tests stay valid."""

EXTRA = {}

EXTRA["vehicle_loan_policy.pdf"] = dict(
    title="Vehicle Loan Policy 2026", docid="POL-VL-2026", version="2.1",
    effective="01 January 2026", owner="Retail Credit Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs loans for the purchase of new and pre-owned passenger "
            "vehicles and two wheelers by resident individual applicants.",
            "Commercial vehicle finance is governed separately and is outside the scope "
            "of this policy."]),
        ("2", "Applicant Eligibility", [
            "- Minimum age at application: 21 years. Maximum age at maturity: 65 years.",
            "- The applicant must hold a valid driving licence at the time of "
            "disbursement.",
            "- The applicant must be a resident Indian citizen with a completed KYC "
            "record."]),
        ("3", "Employment Eligibility", [
            "The applicant must have at least 1 year of total employment history, with a "
            "minimum of 6 months in the current employment or business.",
            "Self-employed applicants must demonstrate 2 years of business vintage."]),
        ("4", "Income Criteria", [
            "- Minimum net monthly income: INR 25,000 for two wheelers and INR 40,000 for "
            "passenger vehicles.",
            "- FOIR inclusive of the proposed EMI must not exceed 55 percent."]),
        ("5", "Loan Amount and Tenure", [
            "- New passenger vehicle: up to 90 percent of ex-showroom price, maximum "
            "tenure 7 years.",
            "- Pre-owned passenger vehicle: up to 75 percent of valuation, maximum tenure "
            "5 years, vehicle age at maturity not exceeding 10 years.",
            "- Two wheeler: up to 85 percent of on-road price, maximum tenure 4 years.",
            "- Maximum loan amount: INR 1,00,00,000."]),
        ("6", "Required Documents", [
            "- Identity proof and address proof as defined in the KYC Policy 2026.",
            "- PAN card, which is mandatory.",
            "- Valid driving licence.",
            "- Latest 3 months salary slips or the latest 2 income tax returns.",
            "- Latest 6 months bank statements.",
            "- Proforma invoice from the dealer."]),
        ("7", "Credit Assessment", [
            "A minimum credit bureau score of 680 is required.",
            "The vehicle must be hypothecated to the bank and the hypothecation endorsed "
            "on the registration certificate within 45 days of disbursement."]),
        ("8", "Insurance", [
            "Comprehensive motor insurance with the bank recorded as financier is "
            "mandatory for the full tenure. Lapse of insurance constitutes an event of "
            "default."]),
        ("9", "Human Review", [
            "No vehicle loan may be approved or rejected by an automated system. The "
            "final decision must be recorded by an authorised credit officer."]),
    ])

EXTRA["fair_practices_code.pdf"] = dict(
    title="Fair Practices Code 2026", docid="POL-FPC-2026", version="3.0",
    effective="01 January 2026", owner="Compliance Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This code sets minimum standards of fair dealing that Horizon National Bank "
            "observes in all interactions with borrowers and prospective borrowers."]),
        ("2", "Applications and Processing", [
            "All communications to the borrower shall be in the vernacular language or a "
            "language understood by the borrower.",
            "Loan application forms shall disclose all information affecting the interest "
            "of the borrower, including the fees payable, and the documents required.",
            "An acknowledgement for receipt of every application shall be given, stating "
            "the indicative time frame for disposal."]),
        ("3", "Appraisal and Terms", [
            "A written sanction letter stating the amount sanctioned, the annualised rate "
            "of interest, the method of application, and all terms and conditions shall "
            "be conveyed to the borrower and the acceptance retained on record.",
            "A Key Facts Statement in a standard format must be provided before the "
            "borrower accepts the offer."]),
        ("4", "Disbursement and Changes in Terms", [
            "Any change in terms and conditions, including disbursement schedule, "
            "interest rate, service charges or prepayment charges, shall be notified to "
            "the borrower in advance. Changes shall be effected prospectively only."]),
        ("5", "Non Interference", [
            "The bank shall refrain from interference in the affairs of the borrower "
            "except for purposes provided in the terms and conditions of the loan "
            "agreement, unless new information not earlier disclosed has come to notice."]),
        ("6", "Recovery Conduct", [
            "The bank shall not resort to undue harassment. Recovery personnel shall not "
            "make calls at odd hours, use abusive language, or contact the borrower's "
            "relatives or employer except as permitted by law.",
            "Contact with the borrower is permitted only between 08:00 and 19:00 hours."]),
        ("7", "Release of Security", [
            "Securities shall be released on repayment of all dues within 30 days, "
            "subject to any legitimate right of lien, which must be notified with full "
            "particulars and the conditions under which the bank is entitled to retain "
            "the security."]),
        ("8", "Grievance Redressal", [
            "Any grievance arising from the application of this code shall be handled "
            "under the Customer Complaint Policy 2026."]),
    ])

EXTRA["data_privacy_policy.pdf"] = dict(
    title="Customer Data Privacy Policy 2026", docid="POL-DP-2026", version="2.0",
    effective="01 January 2026", owner="Chief Information Security Office",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs the collection, processing, storage, sharing and "
            "disposal of customer personal data by Horizon National Bank and its "
            "processors."]),
        ("2", "Lawful Basis and Consent", [
            "Personal data shall be collected only for a specified and lawful purpose "
            "disclosed to the customer at the point of collection.",
            "Consent must be free, specific, informed and capable of being withdrawn as "
            "easily as it was given. Withdrawal of consent shall not affect the lawfulness "
            "of prior processing."]),
        ("3", "Data Minimisation", [
            "Only data necessary for the stated purpose shall be collected. Fields that "
            "are not required for the product applied for shall not be mandatory.",
            "Copies of Officially Valid Documents shall be retained in redacted form "
            "wherever the full document is not required."]),
        ("4", "Masking of Identifiers", [
            "Account numbers, PAN, Aadhaar, customer identifiers, registered mobile "
            "numbers, email addresses and residential addresses shall be masked in all "
            "user interfaces, reports, exports and system generated summaries.",
            "Masking shall occur at the presentation boundary. Systems of record may "
            "retain full values under access control, but no interface, log or downstream "
            "service shall receive an unmasked identifier by default.",
            "Where data is supplied to an automated decisioning or language model "
            "service, identifiers must be masked before transmission."]),
        ("5", "Access Control", [
            "Access to unmasked personal data shall be granted on the principle of least "
            "privilege, tied to a named individual, and reviewed quarterly.",
            "Every access to unmasked data shall generate an audit record containing the "
            "user identity, timestamp, record accessed and stated business purpose."]),
        ("6", "Retention and Disposal", [
            "Personal data shall be retained only for the period required by law or by "
            "the purpose for which it was collected, whichever is longer.",
            "On expiry of the retention period data shall be securely erased or "
            "anonymised, and a certificate of destruction retained."]),
        ("7", "Sharing with Third Parties", [
            "Personal data shall be shared with a third party only under a written "
            "agreement imposing equivalent protection obligations, and only to the extent "
            "necessary.",
            "Cross border transfer requires a documented assessment of the destination "
            "jurisdiction's protections."]),
        ("8", "Breach Notification", [
            "A suspected personal data breach must be reported internally within 6 hours "
            "of detection and to the relevant authority within the period prescribed by "
            "law.",
            "Affected customers shall be notified without undue delay where the breach is "
            "likely to result in harm."]),
        ("9", "Customer Rights", [
            "Customers may request access to, correction of, and erasure of their "
            "personal data, subject to statutory retention obligations. Requests shall be "
            "acknowledged within 3 working days and resolved within 30 days."]),
    ])

EXTRA["digital_banking_policy.pdf"] = dict(
    title="Digital Banking Policy 2026", docid="POL-DB-2026", version="1.4",
    effective="01 January 2026", owner="Digital Channels Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs internet banking, mobile banking and unified payments "
            "interface services offered by Horizon National Bank."]),
        ("2", "Registration and Authentication", [
            "Registration for digital channels requires a fully KYC compliant account and "
            "a registered mobile number.",
            "Two factor authentication is mandatory for all financial transactions. "
            "Biometric authentication may substitute for the second factor on a "
            "registered device."]),
        ("3", "Transaction Limits", [
            "- Unified payments interface: INR 1,00,000 per transaction and INR 1,00,000 "
            "per day by default.",
            "- Internet banking fund transfer to a registered beneficiary: INR 10,00,000 "
            "per day.",
            "- A cooling period of 4 hours applies to newly added beneficiaries, during "
            "which a maximum of INR 5,000 may be transferred.",
            "Customers may request lower limits at any time. Requests to increase limits "
            "require step-up authentication."]),
        ("4", "Unauthorised Transactions and Liability", [
            "- Zero customer liability where the loss is due to a deficiency on the part "
            "of the bank, irrespective of when the customer reports it.",
            "- Zero customer liability for third party breaches where the customer "
            "reports within 3 working days.",
            "- Limited liability where the customer reports between 4 and 7 working days.",
            "- Liability beyond 7 working days is determined by the Board approved policy.",
            "The bank shall credit the disputed amount within 10 working days of "
            "notification, without prejudice to the outcome of the investigation."]),
        ("5", "Service Availability", [
            "Digital channels shall target availability of 99.5 percent measured monthly. "
            "Planned maintenance shall be notified at least 24 hours in advance."]),
        ("6", "Deactivation", [
            "Digital access shall be disabled after 5 consecutive failed authentication "
            "attempts and may be restored only after identity verification.",
            "Channels shall be disabled where the account is classified as inoperative "
            "under the Account Opening Policy 2026."]),
        ("7", "Customer Awareness", [
            "The bank shall not request passwords, one time passwords or card details "
            "through telephone, email or message under any circumstances.",
            "Awareness messages must be displayed at login and sent at least quarterly."]),
    ])

EXTRA["collection_and_recovery_policy.pdf"] = dict(
    title="Collection and Recovery Policy 2026", docid="POL-CR-2026", version="2.2",
    effective="01 January 2026", owner="Credit Administration Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs the collection of overdue amounts and the recovery of "
            "dues from borrowers across all retail lending products."]),
        ("2", "Classification of Overdue Accounts", [
            "- Special Mention Account 0: principal or interest overdue between 1 and 30 "
            "days.",
            "- Special Mention Account 1: overdue between 31 and 60 days.",
            "- Special Mention Account 2: overdue between 61 and 90 days.",
            "- Non-Performing Asset: overdue beyond 90 days."]),
        ("3", "Contact Standards", [
            "Contact with a borrower is permitted only between 08:00 and 19:00 hours on "
            "any day.",
            "Recovery personnel must identify themselves by name and employee or agency "
            "identifier at the start of every interaction.",
            "The use of threatening, abusive or obscene language is prohibited. Any "
            "substantiated instance shall result in termination of the agency engagement."]),
        ("4", "Escalation Sequence", [
            "- Day 1 to 15: automated reminder by message and email.",
            "- Day 16 to 45: telephonic follow up by the collections desk.",
            "- Day 46 to 90: field visit by an authorised representative after prior "
            "intimation.",
            "- Beyond 90 days: formal demand notice and referral to the legal recovery "
            "process."]),
        ("5", "Settlement and Write Off", [
            "A one time settlement may be considered only where recovery of the full dues "
            "is demonstrably unlikely, and requires approval two levels above the "
            "original sanctioning authority.",
            "Every settlement must be reported to the credit information companies with "
            "the correct status."]),
        ("6", "Repossession of Security", [
            "Repossession of a hypothecated asset shall follow the procedure stated in the "
            "loan agreement and applicable law, including prior notice and an opportunity "
            "to regularise.",
            "An inventory of the repossessed asset shall be prepared in the presence of "
            "the borrower or an independent witness."]),
        ("7", "Human Review", [
            "No account shall be referred for legal recovery or settlement solely on the "
            "basis of an automated recommendation. A credit administration officer must "
            "record the decision."]),
        ("8", "Grievances", [
            "Complaints regarding recovery conduct shall be treated as High severity under "
            "the Customer Complaint Policy 2026 and actioned within 1 working day."]),
    ])
