CREATE DATABASE relogio_ponto;
USE relogio_ponto;
CREATE TABLE Funcionarios (
    codigo INTEGER PRIMARY KEY,
    nome TEXT
);

CREATE TABLE RegistrosPonto (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    codigo_funcionario INTEGER,
    tipo_ponto TEXT,
    data TEXT,
    hora TEXT,
    FOREIGN KEY (codigo_funcionario) REFERENCES Funcionarios(codigo)
);


INSERT INTO Funcionarios (codigo, nome) VALUES
(1, 'Andréa'),
(2, 'Tadeu'),
(3, 'Max'),
(4, 'Pedro'),
(5, 'Cássio'),
(6, 'Elaine'),
(7, 'Arthur');

CREATE TABLE Usuarios (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(50) NOT NULL,
    tipo ENUM('admin', 'funcionario') NOT NULL
);

INSERT INTO Usuarios (usuario, senha, tipo) VALUES
('admin', 'admin123', 'admin'),
('funcionario', 'funcionario123', 'funcionario');

ALTER TABLE RegistrosPonto ADD COLUMN data_hora DATETIME;

SHOW TABLES;

UPDATE Funcionarios
SET nome = 'Cássio'
WHERE codigo = '5';

ALTER TABLE RegistrosPonto ADD COLUMN data_hora DATETIME;

-- Desativar o modo de atualização segura temporariamente
SET SQL_SAFE_UPDATES = 0;

-- Excluir todos os registros da tabela Funcionarios
DELETE FROM Funcionarios;

-- Inserir novos registros na tabela Funcionarios
INSERT INTO Funcionarios (codigo, nome) VALUES
(1, 'Andréa'),
(2, 'Tadeu'),
(3, 'Max'),
(4, 'Pedro'),
(7, 'Cássio'),
(11, 'Elaine'),
(17, 'Arthur');

-- Reativar o modo de atualização segura
SET SQL_SAFE_UPDATES = 1;
