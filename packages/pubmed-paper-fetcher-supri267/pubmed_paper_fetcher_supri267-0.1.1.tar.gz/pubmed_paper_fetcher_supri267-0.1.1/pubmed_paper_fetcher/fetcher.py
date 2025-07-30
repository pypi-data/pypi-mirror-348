from typing import List, Tuple, Set, Optional
import requests
import csv
import xml.etree.ElementTree as ET
import re

API_KEY: str = "4bf23c35f17871cdfa7c036b44ea6eca5b09"
API_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
API_URL_DETAILS: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_ids(query: str, debug: bool = False) -> List[str]:
    response = requests.get(API_URL, params={
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'api_key': API_KEY
    })
    if debug:
        print(f"Fetching PubMed IDs for query: {query}")
        print(f"Response: {response.json()}")

    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_id: str, debug: bool = False) -> str:
    response = requests.get(API_URL_DETAILS, params={
        'db': 'pubmed',
        'id': pubmed_id,
        'retmode': 'xml',
        'api_key': API_KEY
    })
    if debug:
        print(f"Fetching details for PubMed ID: {pubmed_id}")
        
    return response.text

def extract_data(pubmed_id: str, details: str, debug: bool = False) -> Tuple[str, str, str, str, str, str]:
    try:
        root: ET.Element = ET.fromstring(details)
    except ET.ParseError:
        return (pubmed_id, "N/A", "N/A", "N/A", "N/A", "N/A")

    title: str = "N/A"
    article: Optional[ET.Element] = root.find(".//Article")
    if article is not None:
        at: Optional[ET.Element] = article.find("ArticleTitle")
        if at is not None and at.text:
            title = at.text.strip()

    pub_date: str = "N/A"
    pubdate_elem: Optional[ET.Element] = root.find(".//PubDate")
    if pubdate_elem is not None:
        year_elem: Optional[ET.Element] = pubdate_elem.find("Year")
        month_elem: Optional[ET.Element] = pubdate_elem.find("Month")
        day_elem: Optional[ET.Element] = pubdate_elem.find("Day")
        if year_elem is not None:
            pub_date = year_elem.text.strip()
            if month_elem is not None:
                pub_date += "-" + month_elem.text.strip()
                if day_elem is not None:
                    pub_date += "-" + day_elem.text.strip()

    non_academic_authors: Set[str] = set()
    company_affiliations: Set[str] = set()
    company_keywords: List[str] = [
        "pharma", "biotech", "inc", "ltd", "corporation", "laboratories", "lab",
        "industries", "research", "systems", "technologies", "healthcare", "consulting",
        "pvt", "llc", "solutions", "clinic", "medical", "hospital", "pharmaceutical",
        "biomedical", "biosciences", "biopharmaceutical", "biotherapeutics", "lifesciences"
    ]

    for author in root.findall(".//Author"):
        fore: Optional[ET.Element] = author.find("ForeName")
        last: Optional[ET.Element] = author.find("LastName")
        
        author_name: str = (
            f"{fore.text.strip()} {last.text.strip()}"
            if fore is not None and last is not None else
            last.text.strip() if last is not None else "Unknown"
        )

        for aff in author.findall(".//AffiliationInfo/Affiliation"):
            affiliation_text: str = aff.text.strip() if aff.text else ""
            if affiliation_text and any(kw in affiliation_text.lower() for kw in company_keywords):
                non_academic_authors.add(author_name)
                if len(affiliation_text) > 100:
                    affiliation_text = affiliation_text[:100] + "..."
                company_affiliations.add(affiliation_text)

    if not non_academic_authors:
        non_academic_authors = {"N/A"}
    if not company_affiliations:
        company_affiliations = {"N/A"}

    company_affiliation_list: List[str] = list(company_affiliations)
    if len(company_affiliation_list) > 5:
        company_affiliation_list = company_affiliation_list[:5]
        company_affiliation_list.append("and more...")

    emails: List[str] = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', details)
    corresponding_email: str = emails[0] if emails else "N/A"

    if debug:
        print(f"Extracted data for {pubmed_id}: Title: {title}, Date: {pub_date}, Email: {corresponding_email}")
    
    return (
        pubmed_id,
        title,
        pub_date,
        "; ".join(sorted(non_academic_authors)),
        "; ".join(company_affiliation_list),
        corresponding_email
    )

def save_to_csv(results: List[Tuple[str, str, str, str, str, str]], filename: str) -> None:
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"
        ])
        for result in results:
            writer.writerow(result)

def print_to_console(results: List[Tuple[str, str, str, str, str, str]]) -> None:
    for result in results:
        print(f"PubmedID: {result[0]}")
        print(f"Title: {result[1]}")
        print(f"Publication Date: {result[2]}")
        print(f"Non-academic Author(s): {result[3]}")
        print(f"Company Affiliation(s): {result[4]}")
        print(f"Corresponding Author Email: {result[5]}")
        print("-" * 80)

