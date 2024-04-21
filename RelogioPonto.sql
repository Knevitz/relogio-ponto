create DATABASE relogio_ponto;
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
(5, 'Cásio'),
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
