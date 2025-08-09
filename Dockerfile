FROM postgres:15

# wal2json qurulması üçün lazım olan alətlər
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-15 \
    && rm -rf /var/lib/apt/lists/*

# wal2json klonla və qur
RUN git clone https://github.com/eulerto/wal2json.git /wal2json && \
    cd /wal2json && \
    make && make install

# Təmizləmə (opsional)
RUN rm -rf /wal2json

# Konfiqurasiya faylları (əgər istəyirsənsə kopyala və dəyişdir)
COPY ./postgresql.conf /etc/postgresql/postgresql.conf
COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
