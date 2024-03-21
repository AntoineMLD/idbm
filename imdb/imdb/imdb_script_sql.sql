/* Répondre aux questions suivantes en SQL :
Quel est le film le plus long ?
Quels sont les 5 films les mieux notés ?
Dans combien de films a joué Morgan Freeman ? Tom Cruise ?
Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ?
Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?
Quel est la durée moyenne d’un film en fonction du genre ?

Bonus :
En fonction du genre, afficher la liste des films les plus longs.
En fonction du genre, quel est le coût de tournage d’une minute de film ?
Quelles sont les séries les mieux notées ?
 */


/* Quel est le film le plus long ? */
select titre, duree, serie 
from public.imdb_data
order by duree desc;

/* Quels sont les 5 films les mieux notés ? */
SELECT titre, score, nombre_vote 
FROM public.imdb_data 
ORDER BY score desc
LIMIT 5;

/* Dans combien de films a joué Morgan Freeman ? Tom Cruise ?*/
SELECT 
    acteur,
    titre AS film,
    COUNT(*) OVER (PARTITION BY acteur) AS nombre_de_films
FROM (
    SELECT 
        'Morgan Freeman' AS acteur, 
        titre
    FROM public.imdb_data
    WHERE casting_principal LIKE '%Morgan Freeman%'
    UNION ALL
    SELECT 
        'Tom Cruise' AS acteur, 
        titre
    FROM public.imdb_data
    WHERE casting_principal LIKE '%Tom Cruise%'
) AS films_par_acteur
ORDER BY acteur, film;

 
/* Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ? */
select titre as film, genre, score
from public.imdb_data id 
where genre like '%Horror'
order by score desc 
limit 3

select titre as film, genre, score
from public.imdb_data id 
where genre like '%Drama'
order by score desc 
limit 3

select titre as film, genre, score
from public.imdb_data id 
where genre like '%Comedy'
order by score desc 
limit 3

/* Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?*/
select 
	SUM(case when pays = 'United States' then 1 else 0 end ) * 100.0 / count(*) as percent_states,
	SUM(case when pays = 'France' then 1 else 0 end) * 100.0 / count(*) as percent_french
from (
 	select titre, pays, score
 	from public.imdb_data 
 	order by score desc
 	limit 10000
 ) as top_100_film
 

 /* Quel est la durée moyenne d’un film en fonction du genre ? */
 select id.genre, avg(id.duree) as duree_moyenne_minutes
 from public.imdb_data id
 group by id.genre
 order by duree_moyenne_minutes desc 
 

/* En fonction du genre, afficher la liste des films les plus longs.*/
with MaxdurationPerGenre as ( 
	select genre, MAX(duree) as MaxDuree
	from public.imdb_data
	group by genre
)
select id.titre, id.genre, id.duree
from public.imdb_data id 
inner join MaxdurationPerGenre mdpg on id.genre = mdpg.genre and id.duree = mdpg.MaxDuree
order by id.genre, id.duree desc;
 