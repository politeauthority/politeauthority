select * from devices where name is not null and last_seen > DATE_SUB(now(), INTERVAL 5 MINUTE) order by last_seen asc;
