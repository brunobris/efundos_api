CREATE TABLE public.fundo (
	id serial NOT NULL,
	codigo varchar(10) NOT NULL,
	acronimo varchar(10) NOT NULL,
	razao_social varchar(150) NOT NULL,
	cnpj varchar(14) NOT NULL,
	administrador varchar(150) NULL,
	data_insercao timestamp NOT NULL,
	data_atualizacao date NOT NULL,
	inativo boolean NOT NULL,
	data_inativado timestamp NULL,
	CONSTRAINT codigo_unique UNIQUE (codigo),
	CONSTRAINT fundo_pkey PRIMARY KEY (id)
);

create table fundo_detalhe (
	id integer primary key references fundo(id),
	liquidez_diaria integer null,
	ultimo_rendimento numeric(4,2) null,
	dividend_yield numeric(4,2) null,
	patrimonio_liquido numeric(12,2) null,
	valor_patrimonial numeric(8,2) null,
	rentabilidade_mes numeric(4,2) null,
	p_vp numeric(4,2) null
);

CREATE TABLE public.fundo_documentos (
	id SERIAL primary KEY,
	fundo_id int4  NOT null references fundo(id),
	fnet_id int4 NOT NULL,
	nome varchar(120) NULL,
	data_publicacao timestamp NULL,
	data_referencia timestamp NULL,
	data_insercao timestamp NOT NULL,
	CONSTRAINT fnet_id_unique UNIQUE (fnet_id)
);

CREATE TABLE public.fundo_dividendos (
	id SERIAL primary KEY,
	fundo_id int4  NOT null references fundo(id),
	rendimento numeric(6,2) NOT NULL,
	data_base date NOT NULL,
	data_pagamento date NOT NULL,
	data_insercao timestamp NOT NULL
);