"""Core policy documents. Thresholds here are load-bearing: backend/validation/rules.py
and the 30-test suite assert against these exact values and section names."""

CORE = {}

CORE["home_loan_policy.pdf"] = dict(
    title="Home Loan Policy 2026", docid="POL-HL-2026", version="4.1",
    effective="01 January 2026", owner="Retail Credit Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs the sourcing, appraisal, sanction, disbursement and "
            "servicing of housing loans extended by Horizon National Bank to resident "
            "individual applicants. It applies to all branches, direct selling agents, "
            "connectors and digital origination channels without exception.",
            "The policy covers loans for purchase of a ready or under-construction "
            "residential property, construction on an owned plot, extension or "
            "improvement of an existing dwelling, and balance transfer of an existing "
            "housing loan from another lender.",
            "Any deviation from the criteria stated in this policy requires written "
            "approval from the Credit Committee, must be supported by documented "
            "compensating factors, and must be recorded in the loan file with the name "
            "and designation of the approving authority.",
            "This policy shall be reviewed annually by the Retail Credit Department and "
            "placed before the Board Credit Committee for approval."]),

        ("2", "Applicant Eligibility", [
            "The applicant must satisfy all of the following conditions:",
            "- The applicant must be a resident Indian citizen.",
            "- The minimum age at the time of application is 21 years.",
            "- The maximum age at loan maturity is 65 years for salaried applicants and "
            "70 years for self-employed applicants.",
            "- The applicant must hold a valid PAN and a completed KYC record as defined "
            "in the KYC Policy 2026.",
            "- A co-applicant is mandatory where the property is jointly owned.",
            "Up to three co-applicants may be added. Income of a co-applicant may be "
            "clubbed only where the co-applicant is a spouse, parent, child or sibling "
            "residing in the same household.",
            "Applicants who are existing borrowers of the bank with any account "
            "classified as Special Mention Account 2 or worse are not eligible until the "
            "account is regularised and remains standard for six consecutive months."]),

        ("3", "Employment Eligibility", [
            "The applicant must have at least 3 years of total employment history. Total "
            "employment history is computed as the aggregate of all verifiable salaried "
            "or self-employed work experience, irrespective of the number of employers.",
            "In addition to the 3 year total employment requirement, salaried applicants "
            "must have completed a minimum of 6 months of continuous service with the "
            "current employer.",
            "Self-employed applicants must demonstrate 3 years of continuous business "
            "vintage supported by audited financial statements or income tax returns for "
            "the last 3 assessment years.",
            "Applicants who do not meet the minimum employment requirement are not "
            "eligible under this policy. Such applications must be declined at the "
            "appraisal stage and may not be escalated for deviation approval.",
            "Employment shall be verified independently through at least two of the "
            "following: employer confirmation on letterhead, salary credit entries in the "
            "bank statement, Employees' Provident Fund contribution history, or Form 16.",
            "A gap in employment exceeding 6 months within the preceding 3 years must be "
            "explained in writing by the applicant and assessed by the credit officer."]),

        ("4", "Income Criteria", [
            "- Minimum net monthly income for salaried applicants: INR 50,000.",
            "- Minimum net annual income for self-employed applicants: INR 7,50,000.",
            "- The Fixed Obligation to Income Ratio (FOIR), inclusive of the proposed "
            "EMI, must not exceed 50 percent of net monthly income.",
            "- Variable pay, incentives and bonuses may be considered at 50 percent of "
            "the average of the last 24 months.",
            "Net monthly income means gross salary less statutory deductions, "
            "professional tax and existing loan instalments recovered at source. "
            "Reimbursements, leave travel allowance and one-time payments are excluded.",
            "Rental income may be considered at 70 percent of the amount evidenced by a "
            "registered lease agreement and reflected in the applicant's bank statement "
            "for at least six months.",
            "Agricultural income shall be considered only where supported by land "
            "records and a certificate from the revenue authority."]),

        ("5", "Loan Amount and Tenure", [
            "- Minimum loan amount: INR 5,00,000.",
            "- Maximum loan amount: INR 10,00,00,000.",
            "- Maximum tenure: 30 years, subject to the maximum age at maturity in "
            "Clause 2.",
            "- Loan to Value ratio must not exceed 90 percent for loans up to "
            "INR 30,00,000, 80 percent for loans above INR 30,00,000 and up to "
            "INR 75,00,000, and 75 percent for loans above INR 75,00,000.",
            "Property value for the purpose of Loan to Value computation is the lower of "
            "the agreement value and the valuation assessed by a panel valuer. Stamp "
            "duty and registration charges are excluded from property value.",
            "Where the property is under construction, disbursement shall be staggered "
            "in line with construction progress certified by the panel architect."]),

        ("6", "Required Documents", [
            "The following documents are required for a home loan application:",
            "- Identity proof (PAN card mandatory, along with Aadhaar, passport, voter ID "
            "or driving licence).",
            "- Address proof (Aadhaar, passport, utility bill not older than 3 months, or "
            "registered rent agreement).",
            "- Income proof (latest 3 months salary slips for salaried applicants; income "
            "tax returns for the last 3 assessment years for self-employed applicants).",
            "- Bank statements for the preceding 6 months of the primary salary or "
            "business account.",
            "- Employment proof (appointment letter, employment certificate, or Form 16 "
            "for the last 2 financial years).",
            "- Property documents (sale agreement, approved building plan, title deed "
            "chain, encumbrance certificate and latest property tax receipt).",
            "Applications with incomplete documentation must not be logged into the "
            "sanctioning system.",
            "Photocopies must be verified against originals by the receiving official, "
            "who shall record the verification on each copy with signature and date."]),

        ("7", "Credit Assessment", [
            "A minimum credit bureau score of 700 is required. Applicants scoring between "
            "650 and 699 may be considered only with a co-applicant meeting the full "
            "income criteria.",
            "Any write-off, settlement or account classified as a Non-Performing Asset in "
            "the applicant's bureau report within the preceding 36 months renders the "
            "application ineligible.",
            "Credit bureau reports must be pulled from at least one licensed credit "
            "information company and must not be older than 30 days at the date of "
            "sanction.",
            "More than three enquiries for unsecured credit in the preceding 90 days "
            "shall be treated as a negative indicator and must be explained in the "
            "appraisal note."]),

        ("8", "Interest Rate and Charges", [
            "- Interest is linked to the external benchmark repo rate plus a spread "
            "determined by the applicant's bureau score and loan to value ratio.",
            "- Processing fee: 0.50 percent of the sanctioned amount, subject to a "
            "maximum of INR 25,000 plus applicable taxes.",
            "- No prepayment charges apply to floating rate loans availed by individual "
            "borrowers.",
            "- Legal and technical verification charges are levied at actuals and "
            "disclosed in the sanction letter.",
            "The spread shall be reset only at the intervals disclosed in the loan "
            "agreement and shall not be altered unilaterally during the tenure."]),

        ("9", "Sanction Authority and Human Review", [
            "No home loan application may be approved or rejected by an automated system. "
            "Decisioning engines and AI assistants may produce eligibility "
            "recommendations only. The final sanction decision must be recorded by an "
            "authorised credit officer.",
            "Sanction authority limits: Branch Manager up to INR 50,00,000; Regional "
            "Credit Head up to INR 3,00,00,000; Credit Committee above INR 3,00,00,000.",
            "The credit officer recording the decision must not be the same person who "
            "sourced the application.",
            "Every recommendation produced by an automated tool must be retained in the "
            "loan file alongside the officer's decision, so that the basis of any "
            "divergence is auditable."]),

        ("10", "Turnaround Time", [
            "- Acknowledgement of application: 1 working day.",
            "- Credit decision after receipt of complete documents: 7 working days.",
            "- Disbursement after execution of loan agreement: 3 working days.",
            "Where a decision cannot be given within the stated time, the applicant must "
            "be informed of the reason and the revised expected date."]),

        ("11", "Property and Legal Due Diligence", [
            "Every property must undergo legal scrutiny by an empanelled advocate and "
            "technical valuation by an empanelled valuer. Both reports must be dated "
            "within 90 days of disbursement.",
            "Properties in areas notified as prohibited, encroached, or subject to "
            "litigation are not eligible for finance.",
            "The title search must cover a minimum period of 30 years or the full chain "
            "of title, whichever is shorter."]),

        ("12", "Insurance", [
            "Property insurance covering fire and allied perils for the full "
            "reconstruction value is mandatory for the entire loan tenure, with the bank "
            "recorded as loss payee.",
            "Credit life insurance is optional. It must not be bundled as a condition of "
            "sanction, and the applicant's written consent must be obtained separately."]),

        ("13", "Monitoring and Default", [
            "End use of funds must be verified within 90 days of final disbursement.",
            "An account is classified as Special Mention Account when the instalment "
            "remains overdue between 31 and 90 days, and as Non-Performing when overdue "
            "beyond 90 days.",
            "Recovery action shall follow the Collection and Recovery Policy 2026. "
            "Coercive practices are prohibited without exception."]),
    ])

CORE["personal_loan_policy.pdf"] = dict(
    title="Personal Loan Policy 2026", docid="POL-PL-2026", version="3.2",
    effective="01 January 2026", owner="Retail Credit Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs unsecured personal loans extended to salaried and "
            "self-employed individuals for permitted end uses. Personal loans may not be "
            "used for speculative investment, capital market trading, or as margin for "
            "other credit facilities.",
            "Permitted end uses include medical expenditure, education expenses, "
            "marriage, travel, home renovation not secured by mortgage, and consolidation "
            "of existing higher-cost debt."]),

        ("2", "Applicant Eligibility", [
            "- Minimum age at application: 23 years. Maximum age at maturity: 60 years.",
            "- The applicant must be a resident Indian citizen with a completed KYC "
            "record.",
            "- Existing customers with a minimum 6 month relationship receive "
            "preferential pricing.",
            "A maximum of two personal loans may be outstanding to the same borrower at "
            "any time, with aggregate exposure not exceeding the limit in Clause 5."]),

        ("3", "Employment Eligibility", [
            "The applicant must have at least 2 years of total employment history, of "
            "which a minimum of 1 year must be with the current employer or in the "
            "current business.",
            "Applicants employed on a contractual or probationary basis are not eligible.",
            "Employment with an employer appearing on the bank's negative or caution list "
            "is not eligible regardless of tenure."]),

        ("4", "Income Criteria", [
            "- Minimum net monthly income: INR 30,000 in metro locations and INR 25,000 "
            "elsewhere.",
            "- FOIR inclusive of the proposed EMI must not exceed 55 percent of net "
            "monthly income.",
            "Salary must be credited to a bank account and evidenced by statements for "
            "the preceding six months. Cash salary is not acceptable."]),

        ("5", "Loan Amount and Tenure", [
            "- Minimum loan amount: INR 50,000. Maximum loan amount: INR 40,00,000.",
            "- Maximum tenure: 7 years.",
            "- The maximum sanctioned amount must not exceed 20 times the net monthly "
            "income."]),

        ("6", "Required Documents", [
            "The following documents are required for a personal loan application:",
            "- Identity proof (PAN card mandatory).",
            "- Address proof.",
            "- Income proof: latest 3 months salary slips, or income tax returns for the "
            "last 2 assessment years for self-employed applicants.",
            "- Bank statements for the preceding 6 months.",
            "- Employment proof or business registration certificate.",
            "Property documents are not required for personal loans as the facility is "
            "unsecured."]),

        ("7", "Credit Assessment", [
            "A minimum credit bureau score of 720 is required for unsecured exposure. No "
            "deviation is permitted below a score of 690.",
            "Aggregate unsecured exposure across all lenders must not exceed 12 times the "
            "applicant's net monthly income after the proposed loan."]),

        ("8", "Charges and Foreclosure", [
            "- Processing fee: up to 2 percent of the sanctioned amount plus applicable "
            "taxes.",
            "- Foreclosure is permitted after 12 EMIs at a charge of 4 percent of the "
            "outstanding principal.",
            "- Late payment charge: 2 percent per month on the overdue instalment.",
            "All charges must be disclosed in the Key Facts Statement provided before "
            "acceptance of the offer."]),

        ("9", "Human Review", [
            "AI assisted eligibility screening is permitted for indicative assessment "
            "only. All sanctions and rejections require authorisation by a credit officer.",
            "Rejection reasons must be communicated to the applicant in writing within 7 "
            "working days of the decision."]),

        ("10", "Turnaround Time", [
            "- Acknowledgement of application: same working day.",
            "- Credit decision after receipt of complete documents: 3 working days.",
            "- Disbursement after acceptance of the sanction letter: 1 working day."]),
    ])

CORE["kyc_policy.pdf"] = dict(
    title="KYC Policy 2026", docid="POL-KYC-2026", version="6.0",
    effective="01 January 2026", owner="Compliance Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy sets out the Know Your Customer framework of Horizon National "
            "Bank in line with applicable regulatory directions. It applies to all "
            "customer relationships across all channels.",
            "The policy is built on four pillars: a Customer Acceptance Policy, Risk "
            "Management, Customer Identification Procedures, and Monitoring of "
            "Transactions."]),

        ("2", "Required Documents for KYC", [
            "A customer must submit one Officially Valid Document for identity and one "
            "for current address. Accepted Officially Valid Documents are:",
            "- Aadhaar number or a masked Aadhaar copy.",
            "- Passport.",
            "- Voter identity card issued by the Election Commission.",
            "- Driving licence.",
            "- Job card issued under the National Rural Employment Guarantee Act.",
            "PAN or Form 60 is mandatory for all accounts in addition to the Officially "
            "Valid Document.",
            "One recent passport size photograph is required for every account holder.",
            "Where the Officially Valid Document does not contain the current address, a "
            "deemed Officially Valid Document such as a utility bill not older than two "
            "months may be accepted, subject to submission of an updated document within "
            "three months."]),

        ("3", "Customer Risk Categorisation", [
            "Every customer must be categorised as Low Risk, Medium Risk or High Risk at "
            "onboarding, based on identity, social and financial status, business "
            "activity, country of origin and expected transaction pattern.",
            "The risk category must be reviewed whenever a material change in customer "
            "profile or transaction behaviour is observed.",
            "Customers engaged in cash intensive businesses, non-resident customers, "
            "trusts with complex ownership, and politically exposed persons shall be "
            "categorised as High Risk by default."]),

        ("4", "KYC Update Frequency", [
            "Periodic updation of KYC records must be carried out at the following "
            "intervals:",
            "- High Risk customers: once every 2 years.",
            "- Medium Risk customers: once every 8 years.",
            "- Low Risk customers: once every 10 years.",
            "Where there is no change in KYC information, a self declaration from the "
            "customer is sufficient to complete periodic updation.",
            "Accounts for which periodic updation is overdue by more than 6 months must "
            "be flagged and may be restricted for debit transactions after prior notice "
            "to the customer.",
            "At least three notices, of which one shall be by registered post, must be "
            "issued before any restriction is applied."]),

        ("5", "Video Based Customer Identification Process", [
            "Video based identification may be used for the onboarding of individual "
            "customers. The session must be conducted by a trained official from a "
            "domestic IP address, must capture a live photograph and PAN, and must be "
            "recorded with an audit trail.",
            "The official must verify liveness through random questions and confirm that "
            "the customer is physically present in India at the time of the session."]),

        ("6", "Enhanced and Simplified Due Diligence", [
            "Enhanced due diligence applies to High Risk customers, politically exposed "
            "persons and non face-to-face onboarding, and requires source of funds "
            "verification and senior management approval.",
            "Simplified due diligence applies to Small Accounts as defined by the "
            "regulator, with balance and turnover limits prescribed therein."]),

        ("7", "Record Retention", [
            "KYC records must be retained for a minimum of 5 years from the date of "
            "cessation of the business relationship. Transaction records must be retained "
            "for 5 years from the date of the transaction.",
            "Records must be retrievable within a reasonable period on request by a "
            "competent authority."]),

        ("8", "Data Protection and Masking", [
            "Aadhaar numbers must be stored in masked form displaying only the last 4 "
            "digits. Account numbers, PAN and contact details must be masked in all "
            "customer facing interfaces and in system generated summaries. Full values "
            "may be revealed only to authorised staff with a documented business need.",
            "Automated systems, including AI assistants, must receive masked values. "
            "Unmasked identifiers must not be transmitted to any model, log, or "
            "third-party service.",
            "Every access to an unmasked identifier must be logged with the user "
            "identity, timestamp and stated business reason."]),

        ("9", "Customer Acceptance", [
            "No account shall be opened in an anonymous or fictitious name.",
            "No account shall be opened where the bank is unable to apply appropriate "
            "due diligence measures.",
            "Customer Acceptance Policy shall not result in denial of banking facility to "
            "members of the general public, especially those who are financially or "
            "socially disadvantaged."]),
    ])

CORE["credit_card_policy.pdf"] = dict(
    title="Credit Card Policy 2026", docid="POL-CC-2026", version="2.4",
    effective="01 January 2026", owner="Cards and Payments Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs the issuance, limit setting, servicing and closure of "
            "credit cards issued by Horizon National Bank."]),
        ("2", "Applicant Eligibility", [
            "- Minimum age at application: 21 years for a primary card and 18 years for "
            "an add on card. Maximum age at application: 65 years.",
            "- Minimum net annual income: INR 3,00,000 for classic variants, "
            "INR 9,00,000 for gold variants and INR 24,00,000 for platinum variants.",
            "- Minimum credit bureau score: 700.",
            "- The applicant must have at least 1 year of total employment history.",
            "No card shall be issued without the explicit written or digital consent of "
            "the applicant. Unsolicited issuance is prohibited."]),
        ("3", "Credit Limit Assignment", [
            "The initial credit limit must not exceed 3 times the net monthly income, "
            "subject to a maximum of INR 15,00,000 across all cards issued to the same "
            "customer.",
            "Limit enhancement may be considered after 12 months of satisfactory conduct "
            "and requires explicit customer consent.",
            "Temporary limit increases require consent for each instance and lapse "
            "automatically at the end of the stated period."]),
        ("4", "Required Documents", [
            "- Identity proof and address proof as defined in the KYC Policy 2026.",
            "- PAN card, which is mandatory.",
            "- Latest 3 months salary slips or the latest income tax return.",
            "- Latest 3 months bank statements."]),
        ("5", "Billing and Charges", [
            "- Interest free credit period: 20 to 50 days, applicable only when the "
            "previous statement balance was paid in full.",
            "- Finance charge: up to 3.5 percent per month on revolved balances.",
            "- Minimum amount due: 5 percent of the statement balance, subject to a "
            "minimum of INR 200.",
            "- Cash advance fee: 2.5 percent of the amount withdrawn, subject to a "
            "minimum of INR 500.",
            "Statements must be dispatched at least 15 days before the payment due date."]),
        ("6", "Dispute and Chargeback", [
            "A transaction dispute must be raised within 60 days of the statement date. "
            "The bank must provide a provisional credit within 7 working days where the "
            "dispute relates to an unauthorised electronic transaction reported within 3 "
            "working days.",
            "Customer liability for unauthorised transactions reported within 3 working "
            "days is nil where the loss is due to a deficiency on the part of the bank."]),
        ("7", "Closure", [
            "A closure request must be processed within 7 working days of receipt, "
            "subject to settlement of all outstanding dues.",
            "Failure to close within 7 working days attracts a penalty of INR 500 per day "
            "of delay payable to the customer."]),
        ("8", "Fair Practices", [
            "Recovery agents must identify themselves and may contact the customer only "
            "between 08:00 and 19:00 hours.",
            "Card details must never be requested over telephone or email by bank staff."]),
    ])

CORE["account_opening_policy.pdf"] = dict(
    title="Account Opening Policy 2026", docid="POL-AO-2026", version="5.1",
    effective="01 January 2026", owner="Retail Banking Operations",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy governs the opening of savings, current and salary accounts for "
            "individual and non individual customers across branch and digital channels."]),
        ("2", "Eligibility", [
            "- Savings accounts may be opened by resident individuals aged 18 years and "
            "above. Minors aged 10 years and above may operate an account independently "
            "subject to limits.",
            "- Current accounts may be opened by proprietorships, partnerships, "
            "companies, limited liability partnerships and trusts.",
            "- A declaration of existing credit facilities with other banks is mandatory "
            "before opening a current account."]),
        ("3", "Required Documents", [
            "- Completed account opening form signed by all account holders.",
            "- Officially Valid Document for identity and address as listed in the KYC "
            "Policy 2026.",
            "- PAN or Form 60.",
            "- Two recent passport size photographs.",
            "- For non individual customers: constitution documents, board resolution or "
            "partnership authority letter, and beneficial ownership declaration."]),
        ("4", "Minimum Balance Requirements", [
            "- Regular savings account: INR 10,000 average monthly balance in metro and "
            "urban branches, INR 5,000 in semi urban branches and INR 2,000 in rural "
            "branches.",
            "- Salary account: no minimum balance requirement while salary credit "
            "continues. The account converts to a regular savings account after 3 "
            "consecutive months without salary credit.",
            "- Basic Savings Bank Deposit Account: no minimum balance requirement.",
            "Charges for non maintenance must be proportionate to the shortfall and must "
            "be notified to the customer at least one month in advance."]),
        ("5", "Account Activation Timelines", [
            "- Accounts opened through video based identification must be activated "
            "within 1 working day of successful verification.",
            "- Branch sourced accounts must be activated within 2 working days of receipt "
            "of complete documentation.",
            "- Where an account opening request fails verification, the customer must be "
            "informed of the specific deficiency within 2 working days and given 15 days "
            "to remediate."]),
        ("6", "Dormancy and Closure", [
            "An account with no customer induced transaction for 24 months must be "
            "classified as inoperative. Reactivation requires fresh KYC verification.",
            "Accounts closed within 12 months of opening attract a closure charge of "
            "INR 500. No charge applies to closures after 12 months.",
            "No charge shall be levied for reactivation of an inoperative account."]),
        ("7", "Nomination", [
            "Nomination facility must be offered to every account holder at the time of "
            "opening. Where the customer declines, the declinature must be recorded in "
            "writing.",
            "A change of nomination must be effected within 3 working days of receipt."]),
    ])

CORE["aml_policy.pdf"] = dict(
    title="Anti-Money Laundering Policy 2026", docid="POL-AML-2026", version="7.0",
    effective="01 January 2026", owner="Compliance Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy establishes the anti money laundering and combating the "
            "financing of terrorism framework of Horizon National Bank and applies to all "
            "employees, agents and outsourced service providers."]),
        ("2", "Designated Officers", [
            "The bank must appoint a Principal Officer responsible for reporting to the "
            "Financial Intelligence Unit and a Designated Director accountable for "
            "overall compliance with this policy.",
            "The Principal Officer shall have direct access to the Board and shall not "
            "hold any role that creates a conflict of interest."]),
        ("3", "Transaction Monitoring Thresholds", [
            "The following transactions must be captured and reported:",
            "- All cash transactions of a value exceeding INR 10,00,000 or the equivalent "
            "in foreign currency.",
            "- All series of integrally connected cash transactions below INR 10,00,000 "
            "that aggregate above that value within a calendar month.",
            "- All cash transactions where forged or counterfeit currency notes have been "
            "used.",
            "- All suspicious transactions, whether or not made in cash, irrespective of "
            "value.",
            "- All cross border wire transfers exceeding INR 5,00,000 where either the "
            "originator or the beneficiary is outside India."]),
        ("4", "Reporting Timelines", [
            "- Cash Transaction Reports must be submitted by the 15th day of the month "
            "following the month of the transaction.",
            "- Suspicious Transaction Reports must be submitted within 7 working days of "
            "the internal conclusion that a transaction is suspicious.",
            "- The customer must not be informed that a Suspicious Transaction Report has "
            "been or will be filed. Tipping off is a punishable offence.",
            "- Counterfeit Currency Reports must be submitted by the 15th day of the "
            "succeeding month."]),
        ("5", "Sanctions Screening", [
            "Every customer must be screened against applicable sanctions lists at "
            "onboarding and rescreened whenever a list is updated. A positive match must "
            "be escalated to the Principal Officer within 1 working day and the "
            "relationship must be frozen pending review.",
            "Screening must cover the customer, beneficial owners, authorised "
            "signatories and counterparties to cross border transactions."]),
        ("6", "Politically Exposed Persons", [
            "Onboarding a politically exposed person requires senior management approval, "
            "source of funds and source of wealth verification, and annual review of the "
            "relationship.",
            "The same treatment applies to close relatives and known associates of a "
            "politically exposed person."]),
        ("7", "Record Keeping and Training", [
            "Records of all reported transactions must be maintained for 5 years from the "
            "date of the transaction. All customer facing staff must complete anti money "
            "laundering training annually.",
            "Training completion must be evidenced by an assessment with a minimum pass "
            "mark of 80 percent."]),
        ("8", "Independent Testing", [
            "The internal audit function shall test the effectiveness of anti money "
            "laundering controls at least annually and report findings to the Audit "
            "Committee of the Board."]),
    ])

CORE["complaint_policy.pdf"] = dict(
    title="Customer Complaint Policy 2026", docid="POL-CMP-2026", version="4.0",
    effective="01 January 2026", owner="Customer Experience Department",
    sections=[
        ("1", "Purpose and Scope", [
            "This policy defines the grievance redressal framework available to customers "
            "of Horizon National Bank and the internal standards for handling complaints."]),
        ("2", "Complaint Channels", [
            "- Branch complaint register and complaint form.",
            "- Customer care telephone line, available 24 hours.",
            "- Internet and mobile banking complaint module.",
            "- Email to the customer care mailbox.",
            "Every complaint must be assigned a unique complaint reference number and "
            "acknowledged within 1 working day.",
            "The complaint reference number must be communicated to the customer through "
            "the same channel on which the complaint was received."]),
        ("3", "Complaint Escalation Process", [
            "Complaints must be escalated through the following levels:",
            "- Level 1: Branch Manager or Customer Care. Resolution within 7 working days.",
            "- Level 2: Regional Nodal Officer, if the customer is not satisfied with the "
            "Level 1 response or if no response is received within 7 working days. "
            "Resolution within 10 working days.",
            "- Level 3: Principal Nodal Officer at Head Office. Resolution within 15 "
            "working days.",
            "- Level 4: The Banking Ombudsman, where the complaint remains unresolved for "
            "30 days from the date of first receipt by the bank, or where the customer is "
            "not satisfied with the reply received.",
            "Contact details for every level must be displayed in all branches and on the "
            "bank's website."]),
        ("4", "Complaint Severity Classification", [
            "- High severity: complaints involving financial loss, unauthorised "
            "transactions, suspected fraud, or repeated failure to respond. Must be "
            "actioned within 1 working day.",
            "- Medium severity: complaints involving service delays, documentation issues "
            "or incorrect charges. Must be actioned within 3 working days.",
            "- Low severity: information requests and general feedback. Must be actioned "
            "within 5 working days.",
            "Severity is determined by the nature of the incident, not by the tone in "
            "which the complaint is expressed."]),
        ("5", "Repeat Complaints", [
            "A complaint reopened by the same customer on the same subject within 30 days "
            "must be automatically escalated one level above the level that issued the "
            "previous response."]),
        ("6", "Compensation", [
            "Where the bank is at fault and the customer has suffered a direct financial "
            "loss, the amount must be reversed along with applicable interest within 10 "
            "working days of the conclusion of the investigation."]),
        ("7", "Reporting", [
            "A consolidated complaint report including volumes, categories, ageing and "
            "root causes must be placed before the Customer Service Committee of the "
            "Board every quarter."]),
        ("8", "Root Cause Analysis", [
            "Any complaint category exceeding 50 instances in a quarter must undergo "
            "documented root cause analysis with a remediation plan and a named owner."]),
    ])
