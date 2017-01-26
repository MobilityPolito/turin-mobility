# 2DO list

* Rendere definitiva la parte di acquisizione dati:

	- Utilizzare lo scheletro degli script in Architecture/*
	- Lanciare i 3 script indipendentemente, con l'utilizzo di supervisor
	- Acquisire i raw data
	- Controllare errori e formato periodicamente tramite DataBaseProxy
	- Comprimere il db: non inserire stati adiacenti uguali
	- Pulire il db: eliminare le features che non useremo mai
	- Formattare il db: unificare il formato dei dati principali per tutti i provider, e mantenere i dati tipici di un certo provider

* Feature extraction:
	
	- Creare collections "fleet" and "zones" (oppure su files)
	- Creare collections "bookings" e "parks"

* Analisi e visualizzazione:

	* Parks:
		- Filtrare per:
			- Business days
			- Weekend days
			- Holiday days
			- Preholiday days
		- Per ogni tipo di giorno, derivare statistiche su:
			- Zona parcheggio
			- Durata parcheggio
		- Per ogni tipo di giorno, visualizzare:
			- Statistiche descrittive
				- Scatter matrix
				- PDF & CDF
				- Boxplots
				- Media e mediana sulle 24 ore
			- Heatmaps
				- Globale
				- Ora per ora (oppure ogni n ore se il grafico è troppo confuso)

	* Books:
		- Considerando T_reservation = 0, Classificare TUTTI i books in:
			- Books (probabilmente) falsi
			- Books "diretti" O != D, T_booking < 120
			- Books "lenti" o "a tappe" O != D, T_booking < 120
			- Possibili tours, O ~ D
			- Possibili noleggi lunghi/giornalieri, T_booking > 120
		- Filtrare per:
			- Business days
			- Weekend days
			- Holiday days
			- Preholiday days
		- Per ogni tipo di giorno, derivare statistiche su:
			- Zona origine
			- Zona destinazione
			- Durata noleggio
			- Distanza noleggio
			- Consumo
			- Matrice OD
		- Per ogni tipo di giorno, visualizzare:
			- Statistiche descrittive
				- Scatter matrix
				- PDF & CDF
				- Boxplots
				- Media e mediana sulle 24 ore
			- (serve o non serve?) Heatmaps origini e destinazioni 
				- Globale
				- Ora per ora (oppure ogni n ore se il grafico è troppo confuso)
			- Matrice OD
		- Introdurre Google
			- Discriminare durate dei viaggi
				- T_booking > T_google and books "Diretti"
					- T_reservation = 0 (-> e.g. viaggio lento)
					- T_reservation = T_booking - T_google
						- T_reservation > free_reservation
						- T_reservation < free_reservation
					- T_reservation = free_reservation
				- T_booking < T_google and books "Diretti"
					- T_reservation = 0 (-> e.g. viaggio veloce)
					- T_reservation > 0 (-> e.g. viaggio super veloce)
		- Transport models (rough)
			- Generation
			- Attraction
			- Distribution
			- Modal choice
* Web application:

	- Menu analytics
	- Interfaccia interattiva
		- Grafico
		- Set parametri
		- Descrizione qualitativa grafico
