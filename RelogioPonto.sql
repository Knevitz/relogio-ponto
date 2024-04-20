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
