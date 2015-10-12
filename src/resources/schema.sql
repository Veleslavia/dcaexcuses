drop table if exists excuses;
create table excuses (
  id integer primary key autoincrement,
  title text not null,
  upvotes integer not null default 0,
  downvotes integer not null default 0
);
insert into excuses (id, title)
  select 0 as id, "кампания уже заведена, но объемы появятся в понедельник" as title
  union select 1, "просто эта стратегия слишком поздно запустилась"
  union select 2, "у нас кластер нестабильный, все падает"
  union select 3 ,"ну а что вы хотели на таком объеме для лукэлайка"
  union select 4,"аналитик энжин упал"
  union select 5,"в новом датацентре этой проблемы не будет"
  union select 6,"мы снизим пороги, и мужчин станет больше. но это будут не совсем мужчины"
  union select 7,"может, дойдет-таки auc хотя бы до 0.8";
