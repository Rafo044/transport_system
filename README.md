# transport_system

CREATE ROLE rep_user WITH REPLICATION LOGIN PASSWORD '12345';



SELECT * FROM pg_create_logical_replication_slot('my_slot', 'wal2json');

