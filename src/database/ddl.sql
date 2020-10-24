CREATE TABLE fundo (
    id serial PRIMARY KEY,
    codigo varchar(10) NOT NULL,
    nome         varchar(150) NOT NULL,
    administrador   varchar(150),
    data_inicio timestamp ,
    data_fim timestamp NULL
);

create table fundo_detalhe (
	id integer primary key references fundo(id),
	liquidez_diaria integer null,
	ultimo_rendimento numeric(4,2) null,
	dividend_yield numeric(4,2) null,
	patrimonio_liquido numeric(12,2) null,
	valor_patrimonial numeric(6,2) null,
	rentabilidade_mes numeric(4,2) null,
	p_vp numeric(4,2) null
)
