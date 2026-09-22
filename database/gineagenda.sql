-- =====================================================
-- GINEAGENDA
-- Banco de Dados e Controle de Versão
-- Banco de dados: MySQL
-- =====================================================

CREATE DATABASE IF NOT EXISTS gineagenda;
USE gineagenda;

-- =====================================================
-- TABELA PACIENTES
-- =====================================================

CREATE TABLE IF NOT EXISTS pacientes (
	id INT NOT NULL AUTO_INCREMENT,
	nome VARCHAR(100) NOT NULL,
	email VARCHAR(120) NOT NULL,
	telefone VARCHAR(20) NOT NULL,
	data_nascimento DATE NOT NULL,
	senha VARCHAR(255) NOT NULL,

	PRIMARY KEY (id),
	UNIQUE (email)
);

-- =====================================================
-- TABELA AGENDAMENTOS
-- =====================================================

CREATE TABLE IF NOT EXISTS agendamentos (
	id INT NOT NULL AUTO_INCREMENT,
	paciente_id INT NOT NULL,
	data_consulta DATE NOT NULL,
	horario TIME NOT NULL,
	status VARCHAR(30) DEFAULT 'Agendada',

	PRIMARY KEY (id),

	CONSTRAINT fk_agendamento_paciente
		FOREIGN KEY (paciente_id)
		REFERENCES pacientes(id)
);

-- =====================================================
-- EXEMPLOS DE MANIPULAÇÃO DE DADOS
-- Utilizar somente para testes.
-- =====================================================

-- INSERT
INSERT INTO pacientes
	(nome, email, telefone, data_nascimento, senha)
VALUES
	('Paciente Teste',
	 'teste@gineagenda.com',
	 '61999999999',
	 '1995-05-10',
	 'senha_teste');

-- SELECT
SELECT id, nome, email, telefone, data_nascimento
FROM pacientes
WHERE email = 'teste@gineagenda.com';

-- UPDATE
UPDATE pacientes
SET telefone = '61888888888'
WHERE email = 'teste@gineagenda.com';

-- Consulta para verificar a atualização
SELECT id, nome, email, telefone
FROM pacientes
WHERE email = 'teste@gineagenda.com';

-- DELETE
DELETE FROM pacientes
WHERE email = 'teste@gineagenda.com';

-- Consulta para verificar a exclusão
SELECT id, nome, email
FROM pacientes
WHERE email = 'teste@gineagenda.com';
