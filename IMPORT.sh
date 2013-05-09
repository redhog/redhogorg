ROOT=/srv/www/redhog.org/django
( cd $ROOT/media/Repositories/literature-dagbok; make; )

appomatic builtinimport
appomatic articlecsvimport $ROOT/media/articles.csv
appomatic articlerssimport $ROOT/media/Repositories/literature-dagbok/diary.rss
appomatic gitimport $ROOT/media/Repositories
appomatic pyimport $ROOT/media/Projects/
appomatic fileimport $ROOT/media/Public/
