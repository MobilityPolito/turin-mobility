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
	
	- Acquisire dati "statici"
	- Creare databases "bookings" e "parkings"
	- Debuggare errore Car2Go (se persiste)
	- Estrarre eventualmente altre features

* Analisi e visualizzazione:

	- Durate parcheggi/noleggi
	- Prezzo noleggi
	- Benzina consumata noleggi
	- Isocrone/Isocosto
	- Zonizzazione -> matrice OD

* Web application:

	- Menu analytics
	- Interfaccia interattiva
		- Grafico
		- Set parametri
		- Descrizione qualitativa grafico
