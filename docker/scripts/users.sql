--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: bluexolo
--

INSERT INTO users VALUES (1, 'pbkdf2_sha256$36000$6Drtc43sNM3n$L5qi6KDdkYrSkme4w2Ezifvmn8T0iT4fRu9DZbVwBZo=', true, 'bluexolo@bluexolo.net', '', '', '2018-08-26 18:12:24.728596+00', '2018-08-26 19:07:21.759393+00', true, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: bluexolo
--

SELECT pg_catalog.setval('users_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

