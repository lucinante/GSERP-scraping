>autore: zhao luca
>data: 18 Giugno 2021
>oggetto: 
	una semplice introduzione al progetto

==========================================================================
>progetto:
	creazione di una classe che è in grado di "raschiare", ordinare e salvare i link relativi alle aziende,
	le quali informazioni sono salvati in una tabular database.

>packages to import:
		-threading
		-os
		-pandas
		-bs4
		-selenium
		-cloudscraper
		-requests

>tabular database format:
		(città)	(azienda)
		citta_1 ,	azienda_1
		citta_1 ,	azienda_2
		citta_2 ,	azienda_3
		   ...
		citta_n ,	azienda_k

>output file format:
		output.txt:
			link1\n
			link2\n
			   ...
			linkn\n

>output directories' structure:
		OUTPUTDIR
			|__news ...
			|
			|__socials ...
			|
			|__others ...
==========================================================================
