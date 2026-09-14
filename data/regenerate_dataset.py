#!/usr/bin/env python3
"""Generate the Bank AI Assistant capstone sample dataset."""
import os, csv, random
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, Image as RLImage)
from reportlab.lib.enums import TA_CENTER
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/claude/dataset"
POL = os.path.join(BASE, "policy-documents")
CUS = os.path.join(BASE, "customer-documents")
SCAN = os.path.join(BASE, "scanned-documents")
MSG = os.path.join(BASE, "customer-messages")
for d in (POL, CUS, SCAN, MSG):
    os.makedirs(d, exist_ok=True)

ss = getSampleStyleSheet()
H0 = ParagraphStyle("H0", parent=ss["Title"], fontSize=16, spaceAfter=4, alignment=TA_CENTER)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontSize=9, alignment=TA_CENTER,
                     textColor=colors.HexColor("#555555"), spaceAfter=14)
H1 = ParagraphStyle("H1", parent=ss["Heading2"], fontSize=12, spaceBefore=12, spaceAfter=5,
                    textColor=colors.HexColor("#0b3d6b"))
BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontSize=9.5, leading=14, spaceAfter=5)
BULL = ParagraphStyle("BULL", parent=BODY, leftIndent=14, bulletIndent=4, spaceAfter=2)


def build_policy(fname, title, docid, version, effective, owner, sections):
    doc = SimpleDocTemplate(os.path.join(POL, fname), pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm, title=title)
    story = [Paragraph("MERIDIAN NATIONAL BANK", H0), Paragraph(title, H0),
             Paragraph(f"Document ID: {docid} &nbsp;|&nbsp; Version {version} &nbsp;|&nbsp; "
                       f"Effective {effective} &nbsp;|&nbsp; Owner: {owner}", SUB)]
    for num, head, paras in sections:
        story.append(Paragraph(f"{num}. {head}", H1))
        for p in paras:
            if p.startswith("- "):
                story.append(Paragraph(p[2:], BULL, bulletText="\u2022"))
            else:
                story.append(Paragraph(p, BODY))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"End of {title}. This document supersedes all prior versions. "
                           f"Queries to be routed to {owner}.", SUB))
    doc.build(story)
    print("  wrote", fname)


# ---------------------------------------------------------------- POLICIES
build_policy(
    "home_loan_policy.pdf", "Home Loan Policy 2026", "POL-HL-2026", "4.1",
    "01 January 2026", "Retail Credit Department",
    [
        ("1", "Purpose and Scope", [
            "This policy governs the sourcing, appraisal, sanction and disbursement of housing "
            "loans extended by Meridian National Bank to resident individual applicants. It applies "
            "to all branches, direct selling agents and digital origination channels.",
            "Any deviation from the criteria stated in this policy requires written approval from "
            "the Credit Committee and must be recorded in the loan file."]),
        ("2", "Applicant Eligibility", [
            "The applicant must satisfy all of the following conditions:",
            "- The applicant must be a resident Indian citizen.",
            "- The minimum age at the time of application is 21 years.",
            "- The maximum age at loan maturity is 65 years for salaried applicants and 70 years "
            "for self-employed applicants.",
            "- The applicant must hold a valid PAN and a completed KYC record as defined in the KYC "
            "Policy 2026.",
            "- A co-applicant is mandatory where the property is jointly owned."]),
        ("3", "Employment Eligibility", [
            "The applicant must have at least 3 years of total employment history. Total employment "
            "history is computed as the aggregate of all verifiable salaried or self-employed work "
            "experience, irrespective of the number of employers.",
            "In addition to the 3 year total employment requirement, salaried applicants must have "
            "completed a minimum of 6 months of continuous service with the current employer.",
            "Self-employed applicants must demonstrate 3 years of continuous business vintage "
            "supported by audited financial statements or income tax returns for the last 3 "
            "assessment years.",
            "Applicants who do not meet the minimum employment requirement are not eligible under "
            "this policy. Such applications must be declined at the appraisal stage and may not be "
            "escalated for deviation approval."]),
        ("4", "Income Criteria", [
            "- Minimum net monthly income for salaried applicants: INR 50,000.",
            "- Minimum net annual income for self-employed applicants: INR 7,50,000.",
            "- The Fixed Obligation to Income Ratio (FOIR), inclusive of the proposed EMI, must not "
            "exceed 50 percent of net monthly income.",
            "- Variable pay, incentives and bonuses may be considered at 50 percent of the average "
            "of the last 24 months."]),
        ("5", "Loan Amount and Tenure", [
            "- Minimum loan amount: INR 5,00,000.",
            "- Maximum loan amount: INR 10,00,00,000.",
            "- Maximum tenure: 30 years, subject to the maximum age at maturity in Clause 2.",
            "- Loan to Value ratio must not exceed 90 percent for loans up to INR 30,00,000, "
            "80 percent for loans above INR 30,00,000 and up to INR 75,00,000, and 75 percent for "
            "loans above INR 75,00,000."]),
        ("6", "Required Documents", [
            "The following documents are required for a home loan application:",
            "- Identity proof (PAN card mandatory, along with Aadhaar, passport, voter ID or "
            "driving licence).",
            "- Address proof (Aadhaar, passport, utility bill not older than 3 months, or "
            "registered rent agreement).",
            "- Income proof (latest 3 months salary slips for salaried applicants; income tax "
            "returns for the last 3 assessment years for self-employed applicants).",
            "- Bank statements for the preceding 6 months of the primary salary or business "
            "account.",
            "- Employment proof (appointment letter, employment certificate, or Form 16 for the "
            "last 2 financial years).",
            "- Property documents (sale agreement, approved building plan, title deed chain, "
            "encumbrance certificate and latest property tax receipt).",
            "Applications with incomplete documentation must not be logged into the sanctioning "
            "system."]),
        ("7", "Credit Assessment", [
            "A minimum credit bureau score of 700 is required. Applicants scoring between 650 and "
            "699 may be considered only with a co-applicant meeting the full income criteria.",
            "Any write-off, settlement or account classified as a Non-Performing Asset in the "
            "applicant's bureau report within the preceding 36 months renders the application "
            "ineligible."]),
        ("8", "Interest Rate and Charges", [
            "- Interest is linked to the external benchmark repo rate plus a spread determined by "
            "the applicant's bureau score and loan to value ratio.",
            "- Processing fee: 0.50 percent of the sanctioned amount, subject to a maximum of "
            "INR 25,000 plus applicable taxes.",
            "- No prepayment charges apply to floating rate loans availed by individual borrowers."]),
        ("9", "Sanction Authority and Human Review", [
            "No home loan application may be approved or rejected by an automated system. "
            "Decisioning engines and AI assistants may produce eligibility recommendations only. "
            "The final sanction decision must be recorded by an authorised credit officer.",
            "Sanction authority limits: Branch Manager up to INR 50,00,000; Regional Credit Head up "
            "to INR 3,00,00,000; Credit Committee above INR 3,00,00,000."]),
        ("10", "Turnaround Time", [
            "- Acknowledgement of application: 1 working day.",
            "- Credit decision after receipt of complete documents: 7 working days.",
            "- Disbursement after execution of loan agreement: 3 working days."]),
    ])

build_policy(
    "personal_loan_policy.pdf", "Personal Loan Policy 2026", "POL-PL-2026", "3.2",
    "01 January 2026", "Retail Credit Department",
    [
        ("1", "Purpose and Scope", [
            "This policy governs unsecured personal loans extended to salaried and self-employed "
            "individuals for permitted end uses. Personal loans may not be used for speculative "
            "investment, capital market trading or as margin for other credit facilities."]),
        ("2", "Applicant Eligibility", [
            "- Minimum age at application: 23 years. Maximum age at maturity: 60 years.",
            "- The applicant must be a resident Indian citizen with a completed KYC record.",
            "- Existing customers with a minimum 6 month relationship receive preferential pricing."]),
        ("3", "Employment Eligibility", [
            "The applicant must have at least 2 years of total employment history, of which a "
            "minimum of 1 year must be with the current employer or in the current business.",
            "Applicants employed on a contractual or probationary basis are not eligible."]),
        ("4", "Income Criteria", [
            "- Minimum net monthly income: INR 30,000 in metro locations and INR 25,000 elsewhere.",
            "- FOIR inclusive of the proposed EMI must not exceed 55 percent of net monthly income."]),
        ("5", "Loan Amount and Tenure", [
            "- Minimum loan amount: INR 50,000. Maximum loan amount: INR 40,00,000.",
            "- Maximum tenure: 7 years.",
            "- The maximum sanctioned amount must not exceed 20 times the net monthly income."]),
        ("6", "Required Documents", [
            "The following documents are required for a personal loan application:",
            "- Identity proof (PAN card mandatory).",
            "- Address proof.",
            "- Income proof: latest 3 months salary slips, or income tax returns for the last 2 "
            "assessment years for self-employed applicants.",
            "- Bank statements for the preceding 6 months.",
            "- Employment proof or business registration certificate.",
            "Property documents are not required for personal loans as the facility is unsecured."]),
        ("7", "Credit Assessment", [
            "A minimum credit bureau score of 720 is required for unsecured exposure. No deviation "
            "is permitted below a score of 690."]),
        ("8", "Charges and Foreclosure", [
            "- Processing fee: up to 2 percent of the sanctioned amount plus applicable taxes.",
            "- Foreclosure is permitted after 12 EMIs at a charge of 4 percent of the outstanding "
            "principal.",
            "- Late payment charge: 2 percent per month on the overdue instalment."]),
        ("9", "Human Review", [
            "AI assisted eligibility screening is permitted for indicative assessment only. All "
            "sanctions and rejections require authorisation by a credit officer."]),
    ])

build_policy(
    "kyc_policy.pdf", "KYC Policy 2026", "POL-KYC-2026", "6.0",
    "01 January 2026", "Compliance Department",
    [
        ("1", "Purpose and Scope", [
            "This policy sets out the Know Your Customer framework of Meridian National Bank in "
            "line with applicable regulatory directions. It applies to all customer relationships "
            "across all channels."]),
        ("2", "Required Documents for KYC", [
            "A customer must submit one Officially Valid Document for identity and one for current "
            "address. Accepted Officially Valid Documents are:",
            "- Aadhaar number or a masked Aadhaar copy.",
            "- Passport.",
            "- Voter identity card issued by the Election Commission.",
            "- Driving licence.",
            "- Job card issued under the National Rural Employment Guarantee Act.",
            "PAN or Form 60 is mandatory for all accounts in addition to the Officially Valid "
            "Document.",
            "One recent passport size photograph is required for every account holder."]),
        ("3", "Customer Risk Categorisation", [
            "Every customer must be categorised as Low Risk, Medium Risk or High Risk at "
            "onboarding, based on identity, social and financial status, business activity, country "
            "of origin and expected transaction pattern.",
            "The risk category must be reviewed whenever a material change in customer profile or "
            "transaction behaviour is observed."]),
        ("4", "KYC Update Frequency", [
            "Periodic updation of KYC records must be carried out at the following intervals:",
            "- High Risk customers: once every 2 years.",
            "- Medium Risk customers: once every 8 years.",
            "- Low Risk customers: once every 10 years.",
            "Where there is no change in KYC information, a self declaration from the customer is "
            "sufficient to complete periodic updation.",
            "Accounts for which periodic updation is overdue by more than 6 months must be flagged "
            "and may be restricted for debit transactions after prior notice to the customer."]),
        ("5", "Video Based Customer Identification Process", [
            "Video based identification may be used for the onboarding of individual customers. "
            "The session must be conducted by a trained official from a domestic IP address, must "
            "capture a live photograph and PAN, and must be recorded with an audit trail."]),
        ("6", "Enhanced and Simplified Due Diligence", [
            "Enhanced due diligence applies to High Risk customers, politically exposed persons and "
            "non face to face onboarding, and requires source of funds verification and senior "
            "management approval.",
            "Simplified due diligence applies to Small Accounts as defined by the regulator, with "
            "balance and turnover limits prescribed therein."]),
        ("7", "Record Retention", [
            "KYC records must be retained for a minimum of 5 years from the date of cessation of "
            "the business relationship. Transaction records must be retained for 5 years from the "
            "date of the transaction."]),
        ("8", "Data Protection and Masking", [
            "Aadhaar numbers must be stored in masked form displaying only the last 4 digits. "
            "Account numbers, PAN and contact details must be masked in all customer facing "
            "interfaces and in system generated summaries. Full values may be revealed only to "
            "authorised staff with a documented business need."]),
    ])

build_policy(
    "credit_card_policy.pdf", "Credit Card Policy 2026", "POL-CC-2026", "2.4",
    "01 January 2026", "Cards and Payments Department",
    [
        ("1", "Purpose and Scope", [
            "This policy governs the issuance, limit setting, servicing and closure of credit cards "
            "issued by Meridian National Bank."]),
        ("2", "Applicant Eligibility", [
            "- Minimum age at application: 21 years for a primary card and 18 years for an add on "
            "card. Maximum age at application: 65 years.",
            "- Minimum net annual income: INR 3,00,000 for classic variants, INR 9,00,000 for gold "
            "variants and INR 24,00,000 for platinum variants.",
            "- Minimum credit bureau score: 700.",
            "- The applicant must have at least 1 year of total employment history."]),
        ("3", "Credit Limit Assignment", [
            "The initial credit limit must not exceed 3 times the net monthly income, subject to a "
            "maximum of INR 15,00,000 across all cards issued to the same customer.",
            "Limit enhancement may be considered after 12 months of satisfactory conduct and "
            "requires explicit customer consent."]),
        ("4", "Required Documents", [
            "- Identity proof and address proof as defined in the KYC Policy 2026.",
            "- PAN card, which is mandatory.",
            "- Latest 3 months salary slips or the latest income tax return.",
            "- Latest 3 months bank statements."]),
        ("5", "Billing and Charges", [
            "- Interest free credit period: 20 to 50 days, applicable only when the previous "
            "statement balance was paid in full.",
            "- Finance charge: up to 3.5 percent per month on revolved balances.",
            "- Minimum amount due: 5 percent of the statement balance, subject to a minimum of "
            "INR 200.",
            "- Cash advance fee: 2.5 percent of the amount withdrawn, subject to a minimum of "
            "INR 500."]),
        ("6", "Dispute and Chargeback", [
            "A transaction dispute must be raised within 60 days of the statement date. The bank "
            "must provide a provisional credit within 7 working days where the dispute relates to "
            "an unauthorised electronic transaction reported within 3 working days."]),
        ("7", "Closure", [
            "A closure request must be processed within 7 working days of receipt, subject to "
            "settlement of all outstanding dues."]),
    ])

build_policy(
    "account_opening_policy.pdf", "Account Opening Policy 2026", "POL-AO-2026", "5.1",
    "01 January 2026", "Retail Banking Operations",
    [
        ("1", "Purpose and Scope", [
            "This policy governs the opening of savings, current and salary accounts for individual "
            "and non individual customers across branch and digital channels."]),
        ("2", "Eligibility", [
            "- Savings accounts may be opened by resident individuals aged 18 years and above. "
            "Minors aged 10 years and above may operate an account independently subject to limits.",
            "- Current accounts may be opened by proprietorships, partnerships, companies, limited "
            "liability partnerships and trusts.",
            "- A declaration of existing credit facilities with other banks is mandatory before "
            "opening a current account."]),
        ("3", "Required Documents", [
            "- Completed account opening form signed by all account holders.",
            "- Officially Valid Document for identity and address as listed in the KYC Policy 2026.",
            "- PAN or Form 60.",
            "- Two recent passport size photographs.",
            "- For non individual customers: constitution documents, board resolution or partnership "
            "authority letter, and beneficial ownership declaration."]),
        ("4", "Minimum Balance Requirements", [
            "- Regular savings account: INR 10,000 average monthly balance in metro and urban "
            "branches, INR 5,000 in semi urban branches and INR 2,000 in rural branches.",
            "- Salary account: no minimum balance requirement while salary credit continues. The "
            "account converts to a regular savings account after 3 consecutive months without "
            "salary credit.",
            "- Basic Savings Bank Deposit Account: no minimum balance requirement."]),
        ("5", "Account Activation Timelines", [
            "- Accounts opened through video based identification must be activated within 1 "
            "working day of successful verification.",
            "- Branch sourced accounts must be activated within 2 working days of receipt of "
            "complete documentation.",
            "- Where an account opening request fails verification, the customer must be informed "
            "of the specific deficiency within 2 working days and given 15 days to remediate."]),
        ("6", "Dormancy and Closure", [
            "An account with no customer induced transaction for 24 months must be classified as "
            "inoperative. Reactivation requires fresh KYC verification.",
            "Accounts closed within 12 months of opening attract a closure charge of INR 500. No "
            "charge applies to closures after 12 months."]),
    ])

build_policy(
    "aml_policy.pdf", "Anti-Money Laundering Policy 2026", "POL-AML-2026", "7.0",
    "01 January 2026", "Compliance Department",
    [
        ("1", "Purpose and Scope", [
            "This policy establishes the anti money laundering and combating the financing of "
            "terrorism framework of Meridian National Bank and applies to all employees, agents and "
            "outsourced service providers."]),
        ("2", "Designated Officers", [
            "The bank must appoint a Principal Officer responsible for reporting to the Financial "
            "Intelligence Unit and a Designated Director accountable for overall compliance with "
            "this policy."]),
        ("3", "Transaction Monitoring Thresholds", [
            "The following transactions must be captured and reported:",
            "- All cash transactions of a value exceeding INR 10,00,000 or the equivalent in "
            "foreign currency.",
            "- All series of integrally connected cash transactions below INR 10,00,000 that "
            "aggregate above that value within a calendar month.",
            "- All cash transactions where forged or counterfeit currency notes have been used.",
            "- All suspicious transactions, whether or not made in cash, irrespective of value."]),
        ("4", "Reporting Timelines", [
            "- Cash Transaction Reports must be submitted by the 15th day of the month following "
            "the month of the transaction.",
            "- Suspicious Transaction Reports must be submitted within 7 working days of the "
            "internal conclusion that a transaction is suspicious.",
            "- The customer must not be informed that a Suspicious Transaction Report has been or "
            "will be filed. Tipping off is a punishable offence."]),
        ("5", "Sanctions Screening", [
            "Every customer must be screened against applicable sanctions lists at onboarding and "
            "rescreened whenever a list is updated. A positive match must be escalated to the "
            "Principal Officer within 1 working day and the relationship must be frozen pending "
            "review."]),
        ("6", "Politically Exposed Persons", [
            "Onboarding a politically exposed person requires senior management approval, source of "
            "funds and source of wealth verification, and annual review of the relationship."]),
        ("7", "Record Keeping and Training", [
            "Records of all reported transactions must be maintained for 5 years from the date of "
            "the transaction. All customer facing staff must complete anti money laundering "
            "training annually."]),
    ])

build_policy(
    "complaint_policy.pdf", "Customer Complaint Policy 2026", "POL-CMP-2026", "4.0",
    "01 January 2026", "Customer Experience Department",
    [
        ("1", "Purpose and Scope", [
            "This policy defines the grievance redressal framework available to customers of "
            "Meridian National Bank and the internal standards for handling complaints."]),
        ("2", "Complaint Channels", [
            "- Branch complaint register and complaint form.",
            "- Customer care telephone line, available 24 hours.",
            "- Internet and mobile banking complaint module.",
            "- Email to the customer care mailbox.",
            "Every complaint must be assigned a unique complaint reference number and acknowledged "
            "within 1 working day."]),
        ("3", "Complaint Escalation Process", [
            "Complaints must be escalated through the following levels:",
            "- Level 1: Branch Manager or Customer Care. Resolution within 7 working days.",
            "- Level 2: Regional Nodal Officer, if the customer is not satisfied with the Level 1 "
            "response or if no response is received within 7 working days. Resolution within 10 "
            "working days.",
            "- Level 3: Principal Nodal Officer at Head Office. Resolution within 15 working days.",
            "- Level 4: The Banking Ombudsman, where the complaint remains unresolved for 30 days "
            "from the date of first receipt by the bank, or where the customer is not satisfied "
            "with the reply received."]),
        ("4", "Complaint Severity Classification", [
            "- High severity: complaints involving financial loss, unauthorised transactions, "
            "suspected fraud, or repeated failure to respond. Must be actioned within 1 working day.",
            "- Medium severity: complaints involving service delays, documentation issues or "
            "incorrect charges. Must be actioned within 3 working days.",
            "- Low severity: information requests and general feedback. Must be actioned within 5 "
            "working days."]),
        ("5", "Repeat Complaints", [
            "A complaint reopened by the same customer on the same subject within 30 days must be "
            "automatically escalated one level above the level that issued the previous response."]),
        ("6", "Compensation", [
            "Where the bank is at fault and the customer has suffered a direct financial loss, the "
            "amount must be reversed along with applicable interest within 10 working days of the "
            "conclusion of the investigation."]),
        ("7", "Reporting", [
            "A consolidated complaint report including volumes, categories, ageing and root causes "
            "must be placed before the Customer Service Committee of the Board every quarter."]),
    ])

# ------------------------------------------------------ CUSTOMER LOAN FORMS
CUSTOMERS = [
    dict(cid="C1001", name="Rahul Sharma", loan="Home Loan", amount=7500000, income=125000,
         emp="Salaried", exp="2 years", cur_emp="1 year 4 months", dob="12/08/1993",
         pan="ABCDE1234F", aadhaar="XXXX XXXX 4821", mobile="+91 98XXXXXX21",
         email="rahul.sharma@example.com", employer="Nexline Technologies Pvt Ltd",
         city="Pune", tenure=20, bureau=744, obligations=18000, prop="Flat 402, Aster Residency, Pune"),
    dict(cid="C1002", name="Priya Menon", loan="Home Loan", amount=4200000, income=98000,
         emp="Salaried", exp="7 years", cur_emp="4 years 2 months", dob="03/02/1989",
         pan="BQRST5678K", aadhaar="XXXX XXXX 1190", mobile="+91 97XXXXXX08",
         email="priya.menon@example.com", employer="Calder Life Insurance Ltd",
         city="Kochi", tenure=18, bureau=781, obligations=9500, prop="Villa 11, Palm Grove, Kochi"),
    dict(cid="C1003", name="Imran Qureshi", loan="Personal Loan", amount=900000, income=64000,
         emp="Salaried", exp="3 years", cur_emp="2 years 6 months", dob="19/11/1994",
         pan="CDEFG9012M", aadhaar="XXXX XXXX 7742", mobile="+91 99XXXXXX63",
         email="imran.qureshi@example.com", employer="Vanta Logistics India Ltd",
         city="Hyderabad", tenure=5, bureau=712, obligations=6000, prop="Not applicable"),
    dict(cid="C1004", name="Ananya Iyer", loan="Home Loan", amount=11500000, income=310000,
         emp="Self-Employed", exp="9 years", cur_emp="9 years", dob="27/05/1986",
         pan="DEFGH3456P", aadhaar="XXXX XXXX 3308", mobile="+91 96XXXXXX17",
         email="ananya.iyer@example.com", employer="Iyer Design Studio (Proprietorship)",
         city="Bengaluru", tenure=25, bureau=698, obligations=42000, prop="Plot 7, Whitefield, Bengaluru"),
    dict(cid="C1005", name="Vikram Desai", loan="Personal Loan", amount=1500000, income=41000,
         emp="Salaried", exp="4 years", cur_emp="8 months", dob="09/03/1996",
         pan="EFGHI7890R", aadhaar="XXXX XXXX 9051", mobile="+91 95XXXXXX74",
         email="vikram.desai@example.com", employer="Brightpath Retail Pvt Ltd",
         city="Ahmedabad", tenure=6, bureau=669, obligations=11000, prop="Not applicable"),
]

FIELD_LABEL = ParagraphStyle("FL", parent=BODY, fontSize=9, textColor=colors.HexColor("#333333"))


def inr(n):
    s = str(n)
    if len(s) <= 3:
        return "INR " + s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head:
        parts.insert(0, head)
    return "INR " + ",".join(parts) + "," + tail


def build_application(c):
    fname = f"customer_{c['cid'][1:]}_{c['loan'].split()[0].lower()}_loan_application.pdf"
    doc = SimpleDocTemplate(os.path.join(CUS, fname), pagesize=A4,
                            leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title=f"{c['loan']} Application {c['cid']}")
    story = [Paragraph("MERIDIAN NATIONAL BANK", H0),
             Paragraph(f"{c['loan']} Application Form", H0),
             Paragraph(f"Application Reference: APP-{c['cid']}-2026 &nbsp;|&nbsp; "
                       f"Branch: {c['city']} Main &nbsp;|&nbsp; Date: 14/02/2026", SUB)]

    def block(head, rows):
        story.append(Paragraph(head, H1))
        t = Table([[Paragraph(f"<b>{k}</b>", FIELD_LABEL), Paragraph(str(v), FIELD_LABEL)]
                   for k, v in rows], colWidths=[62 * mm, 100 * mm])
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b9c6d4")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef3f8")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]))
        story.append(t)

    block("Section A - Applicant Details", [
        ("Customer ID", c["cid"]), ("Applicant Name", c["name"]),
        ("Date of Birth", c["dob"]), ("PAN Number", c["pan"]),
        ("Aadhaar Number", c["aadhaar"]), ("Mobile Number", c["mobile"]),
        ("Email Address", c["email"]), ("City", c["city"]),
        ("Residential Status", "Resident Indian")])
    block("Section B - Employment Details", [
        ("Employment Type", c["emp"]), ("Employer / Business Name", c["employer"]),
        ("Total Employment History", c["exp"]),
        ("Experience with Current Employer", c["cur_emp"]),
        ("Net Monthly Income", inr(c["income"])),
        ("Existing Monthly Obligations", inr(c["obligations"]))])
    block("Section C - Loan Request", [
        ("Loan Type", c["loan"]), ("Requested Loan Amount", inr(c["amount"])),
        ("Requested Tenure", f"{c['tenure']} years"),
        ("Purpose", "Purchase of residential property" if c["loan"] == "Home Loan"
         else "Personal expenditure"),
        ("Property Address", c["prop"]),
        ("Credit Bureau Score", c["bureau"])])
    block("Section D - Documents Submitted", [
        ("Identity Proof", "Submitted"), ("Address Proof", "Submitted"),
        ("Income Proof", "Submitted"), ("Bank Statements (6 months)", "Submitted"),
        ("Employment Proof", "Submitted"),
        ("Property Documents", "Submitted" if c["loan"] == "Home Loan" else "Not applicable")])
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Declaration: I confirm that the information furnished above is true and complete to the "
        "best of my knowledge. I authorise Meridian National Bank to verify the information and to "
        "obtain my credit information report from any credit information company.", BODY))
    story.append(Spacer(1, 14))
    story.append(Paragraph(f"Signature: ______________________ &nbsp;&nbsp;&nbsp; "
                           f"Name: {c['name']} &nbsp;&nbsp;&nbsp; Date: 14/02/2026", BODY))
    story.append(Spacer(1, 10))
    story.append(Paragraph("FOR BANK USE ONLY - Appraisal Notes", H1))
    story.append(Paragraph("Verified by: ____________ &nbsp; Credit Officer ID: ____________ &nbsp; "
                           "Recommendation: ____________ &nbsp; Sanction Authority: ____________", BODY))
    doc.build(story)
    print("  wrote", fname)


# ------------------------------------------- SCANNED (IMAGE-ONLY) DOCUMENTS
def _font(sz, bold=False):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except OSError:
            continue
    return ImageFont.load_default()


def scanned_pdf(fname, lines, width=1240, height=1754, rotate=0.45, noise=True):
    img = Image.new("L", (width, height), 246)
    d = ImageDraw.Draw(img)
    y = 90
    for text, sz, bold in lines:
        if text == "__RULE__":
            d.line([(90, y + 6), (width - 90, y + 6)], fill=120, width=2); y += 26; continue
        d.text((90, y), text, font=_font(sz, bold), fill=35)
        y += int(sz * 1.85)
    if noise:
        px = img.load()
        for _ in range(int(width * height * 0.012)):
            x, yy = random.randrange(width), random.randrange(height)
            px[x, yy] = max(0, px[x, yy] - random.randrange(25, 70))
    img = img.rotate(rotate, resample=Image.BICUBIC, fillcolor=246, expand=False)
    path = os.path.join(SCAN, fname)
    img.convert("RGB").save(path, "PDF", resolution=150.0)
    print("  wrote", fname, "(image-only, requires OCR)")


random.seed(7)
scanned_pdf("customer_1001_bank_statement_scanned.pdf", [
    ("MERIDIAN NATIONAL BANK", 34, True),
    ("Statement of Account", 24, False), ("__RULE__", 0, False),
    ("Account Number  : 90210041234", 21, False),
    ("Customer Name   : Rahul Sharma", 21, False),
    ("Customer ID     : C1001", 21, False),
    ("IFSC Code       : MNBK0000412", 21, False),
    ("Branch          : Pune Main", 21, False),
    ("Statement Period: 01 Jan 2026 to 31 Mar 2026", 21, False),
    ("PAN             : ABCDE1234F", 21, False),
    ("Registered Mobile: +91 9822104821", 21, False), ("__RULE__", 0, False),
    ("DATE        DESCRIPTION                    DEBIT      CREDIT     BALANCE", 18, True),
    ("05-01-2026  SALARY NEXLINE TECHNOLOGIES        -     125000     318420", 18, False),
    ("07-01-2026  UPI/RENT/LANDLORD               28000          -     290420", 18, False),
    ("12-01-2026  EMI AUTO LOAN 44120182          18000          -     272420", 18, False),
    ("22-01-2026  CARD PAYMENT MNB PLATINUM       14200          -     258220", 18, False),
    ("05-02-2026  SALARY NEXLINE TECHNOLOGIES         -     125000     383220", 18, False),
    ("07-02-2026  UPI/RENT/LANDLORD               28000          -     355220", 18, False),
    ("12-02-2026  EMI AUTO LOAN 44120182          18000          -     337220", 18, False),
    ("28-02-2026  NEFT/INSURANCE PREMIUM          22500          -     314720", 18, False),
    ("05-03-2026  SALARY NEXLINE TECHNOLOGIES         -     125000     439720", 18, False),
    ("07-03-2026  UPI/RENT/LANDLORD               28000          -     411720", 18, False),
    ("12-03-2026  EMI AUTO LOAN 44120182          18000          -     393720", 18, False),
    ("__RULE__", 0, False),
    ("Opening Balance : 221420        Closing Balance : 393720", 19, False),
    ("Total Credits   : 375000        Total Debits    : 202700", 19, False),
    ("Average Monthly Balance : 331287", 19, False), ("__RULE__", 0, False),
    ("This is a computer generated statement and does not require a signature.", 16, False),
])

scanned_pdf("customer_1001_identity_card_scanned.pdf", [
    ("INCOME TAX DEPARTMENT          GOVT OF INDIA", 22, True), ("__RULE__", 0, False),
    ("Permanent Account Number Card", 26, True),
    ("", 10, False),
    ("Name            : RAHUL SHARMA", 24, False),
    ("Father's Name   : MAHESH SHARMA", 24, False),
    ("Date of Birth   : 12/08/1993", 24, False),
    ("Permanent Account Number", 20, False),
    ("ABCDE1234F", 40, True),
    ("", 10, False), ("__RULE__", 0, False),
    ("Signature : R. Sharma", 22, False),
    ("", 8, False),
    ("Specimen document generated for the Meridian National Bank AI capstone project.", 15, False),
    ("Not a real identity document. Contains no real personal data.", 15, False),
], height=900, rotate=-0.8)

# ------------------------------------------------------- CUSTOMER MESSAGES
MESSAGES = [
    ("C1001", "My home loan application has been pending for three weeks and nobody from the branch has called me back. I have already submitted my documents twice.", "Loan"),
    ("C1002", "Could you please tell me the current status of my home loan application? I submitted it on 14 February.", "Loan"),
    ("C1003", "I have tried to update my KYC on the mobile app four times and it keeps failing at the Aadhaar step. This is extremely frustrating and no one is helping.", "KYC"),
    ("C1004", "Thank you for the quick turnaround on my property valuation. The relationship manager was very helpful throughout.", "Loan"),
    ("C1005", "My account opening request failed and I was never told why. I have wasted two visits to the branch.", "Account"),
    ("C1006", "I raised a complaint about an unauthorised card transaction of 14,200 rupees eleven days ago and I have still not received the provisional credit. I will escalate this to the ombudsman.", "Complaint"),
    ("C1007", "I want to know whether I am eligible for a personal loan with a net monthly income of 34,000 rupees.", "Loan"),
    ("C1008", "The minimum balance charge levied on my salary account last month appears to be incorrect. Please review it.", "Account"),
    ("C1009", "Please confirm which documents I need to submit for periodic KYC updation. My account is categorised as low risk.", "KYC"),
    ("C1010", "Absolutely appalling service. Three visits, two phone calls, zero answers about my loan. I am closing every account I have with this bank.", "Complaint"),
    ("C1011", "The new mobile app is much faster than the old one. Very happy with the update.", "General"),
    ("C1012", "My credit card limit enhancement request was rejected without any explanation. Can someone tell me the reason?", "Card"),
    ("C1013", "I need my home loan sanction letter reissued with a corrected spelling of my name.", "Loan"),
    ("C1014", "Nobody has responded to my complaint reference CMP-2026-8841 for over a month now. This is unacceptable.", "Complaint"),
    ("C1015", "What is the processing fee for a home loan of 50 lakh rupees?", "Loan"),
]
csv_path = os.path.join(MSG, "customer_messages.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["customer_id", "message", "category"])
    w.writerows(MESSAGES)
print("  wrote customer_messages.csv")

print("Building customer applications...")
for c in CUSTOMERS:
    build_application(c)

print("\nDataset complete.")
for root, _, files in os.walk(BASE):
    for fl in sorted(files):
        print(" ", os.path.relpath(os.path.join(root, fl), BASE))
