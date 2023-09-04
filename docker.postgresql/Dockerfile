FROM ivanlonel/postgis-with-extensions:14-3.2

LABEL authors="Endrigo Rivas <endrigo.rivas@cosmesoft.com.py>"

# Install utilities
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y postgresql-14-partman
RUN apt-get install -y pg-activity
RUN apt-get install -y pgtop
RUN apt-get install -y postgresql-14-pldebugger
RUN apt-get install -y unzip


# Clear package lists
RUN apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

