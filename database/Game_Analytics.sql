CREATE DATABASE tennis_db;
USE tennis_db;

CREATE TABLE Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    abbreviation VARCHAR(10) NOT NULL
);

CREATE TABLE Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

CREATE TABLE Rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    ranks INT NOT NULL,
    movement INT NOT NULL,
    points INT NOT NULL,
    competitions_played INT NOT NULL,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
);

CREATE TABLE Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code CHAR(3) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);

-- 1) Categories & Competitions

-- List all competitions along with their category name
select c.competition_name, cat.category_name
from competitions c 
join categories cat on c.category_id = cat.category_id;

-- Count the number of competitions in each category
 select cat.category_name, count(*) as total_competitions
from competitions c
join categories cat on c.category_id = cat.category_id
group by cat.category_name
order by total_competitions DESC;

-- Find all competitions of type 'doubles'
select competition_name, type
from competitions
WHERE type like '%doubles%';

-- Get competitions that belong to a specific category (e.g., ITF Men)
select c.competition_name, cat.category_name
from competitions c
join categories cat on c.category_id = cat.category_id
where cat.category_name = 'ITF Men';

-- Identify parent competitions and their sub-competitions
select p.competition_name as parent_competition, c.competition_name as sub_competition
from competitions p
join competitions c 
on p.competition_id = c.parent_id;

-- Analyze the distribution of competition types by category
select cat.category_name, c.type, count(*) AS total
from competitions c
join categories cat 
on c.category_id = cat.category_id
group by cat.category_name, c.type
order by cat.category_name;

-- List all competitions with no parent (top-level competitions)
select competition_name
from competitions
where parent_id is null;

-- 2) Complexes & Venues

-- List all venues along with their associated complex name
select v.venue_name, c.complex_name
from venues v
join complexes c 
ON v.complex_id = c.complex_id;

-- Count the number of venues in each complex
select c.complex_name, count(*) as total_venues
from venues v
join complexes c on v.complex_id = c.complex_id
group by c.complex_name
order by total_venues desc;

-- Get details of venues in a specific country (e.g., Chile)
select venue_name, city_name, country_name
from venues
where country_name = 'chile';

-- Identify all venues and their timezones
select venue_name, timezone
FROM venues;

-- Find complexes that have more than one venue
select c.complex_id, c.complex_name, count(*) as total_venues
from venues v
join complexes c on c.complex_id = v.complex_id
group by c.complex_id, c.complex_name
having count(*) > 1;

-- List venues grouped by country
select country_name, count(*) as total_venues
from venues
group by country_name
order by total_venues desc;

-- Find all venues for a specific complex (e.g., Nacional)
select v.venue_name, c.complex_name
from venues v
join complexes c on v.complex_id = c.complex_id
where c.complex_name = 'Nacional';

-- 3) #Rankings & Competitors

-- Get all competitors with their rank and points
select c.name as competitor_name, r.ranks, r.points
from rankings r
join competitors c on r.competitor_id = c.competitor_id
order by r.ranks;

-- Find competitors ranked in the top 5
select c.name, r.ranks
from rankings r
join competitors c on r.competitor_id = c.competitor_id
where r.ranks <= 5
order by r.ranks;

-- List competitors with no rank movement (stable rank)
select c.name, r.ranks, r.movement
from rankings r
join competitors c on r.competitor_id = c.competitor_id
where r.movement = 0;

-- Get total points of competitors from a specific country (e.g., Croatia)
select c.country, sum(r.points) as total_points
from rankings r
join competitors c on r.competitor_id = c.competitor_id
where c.country = 'Croatia'
group by c.country;

-- Count the number of competitors per country
select country, count(*) AS total_competitors
from competitors
group by country
order by total_competitors desc;

-- Find competitors with the highest points in the current week
select c.name, r.points
from rankings r
join competitors c 
on r.competitor_id = c.competitor_id
where r.points = (select max(points) from rankings);
