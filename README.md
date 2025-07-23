# SEC data analysis and summarization
providing insights into mutual fund investments and company financials

## The Mission
### Observe what stocks mutual funds own and track how that changes over time.
1. Which mutual funds are we tracking
2. Find their official ID number (CIK)
3. Use that ID to pull their holdings from the SEC
4. Analyze those reports to see what stocks/bonds they hold
5. Build insights

## Notes and Comments
### Scraping the CIK for each mutual fund
To pull the CIKs of the MF_O mutual funds (no duplicates (4842 entries)), 3628 entity ciks were found. This is using the web scraping tecnique. It took 27 mins and 22 secs. Now to pull the ciks with the series ciks, it took 34 mins and 25 secs. Still 3628 entity ciks found. 

The name, CIK, and Series CIK for each notable mutual fund (MF_O) are stored in a CSV file. For now, the 1214 names without a corresponding CIK will be ignored. Having the CIK is crucial for programmatically accessing data from the SEC.

### Identifying the relevant filings for each mutual fund
Mutual funds report their holdings and portfolio information, along with a slew of other data required by the SEC, in a submission. The entire list of submissions of a mutual fund can be viewed using the SEC API. For financial/portfolio information, the NPORT-P filing is of most interest. Presented in either xml or html, identifying and selecting the files is straighforward. Then, using BeautifulSoup, the entire NPORT file is parsed and prepared to be fed to the LLM.

### Analyzing and summarizing with AI
GPT is plenty capable of providing profound insights for financial information, so OpenAI API model GPT-4o-mini is used to provide the insights of a file. A properly engineered prompt and low temperature (0.1-0.2) mean that formatting can be relatively consistent throughout multiple analyses.

### Next Steps
Currently the model only reads one file (from a hardcoded CIK) and prints output. Next steps include:
<br>+ Pulling the CIKs for multiple mutual funds from the CSV file (array for speed and ease)
<br>+ Saving the output/insights to a file
<br>+ Using multiple filings from a company over time to generate trends (this would require adding context to the AI)
<br>+ Using the insights from multiple mutual funds to detect industry/sector/era trends
<br>+ Incorporate macro data from other federal sources and media to complement insights