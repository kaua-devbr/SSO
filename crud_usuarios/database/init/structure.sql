''
USE UNIFICA;

CREATE TABLE usuarios (
    usuario_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    oidc_issuer VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin NULL,
    oidc_sub VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin NULL,
    nome_completo VARCHAR(150) NOT NULL,
    email VARCHAR(254) NULL,
    data_nascimento DATE NULL,
    apelido VARCHAR(60) NULL,
    cidade VARCHAR(100) NULL,
    uf CHAR(2) NULL,
    genero VARCHAR(50) NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (usuario_id),
    UNIQUE KEY uq_usuario_identidade (oidc_issuer, oidc_sub),
    CONSTRAINT ck_usuario_identidade CHECK (
      (oidc_issuer IS NULL AND oidc_sub IS NULL) OR
      (oidc_issuer IS NOT NULL AND oidc_sub IS NOT NULL AND CHAR_LENGTH(oidc_issuer)>0 AND CHAR_LENGTH(oidc_sub)>0)),
    CONSTRAINT ck_usuario_nome CHECK (CHAR_LENGTH(TRIM(nome_completo)) > 0),
    CONSTRAINT ck_usuario_ativo CHECK (ativo IN (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE escolas (
    escola_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100) NULL,
    uf CHAR(2) NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT ck_escola_nome CHECK (CHAR_LENGTH(TRIM(nome))>0),
    CONSTRAINT ck_escola_ativo CHECK (ativo IN (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE turmas (
    turma_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    escola_id BIGINT UNSIGNED NOT NULL,
    nome VARCHAR(60) NOT NULL,
    ano_letivo SMALLINT UNSIGNED NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE KEY uq_turma (escola_id, ano_letivo, nome),
    CONSTRAINT fk_turma_escola FOREIGN KEY (escola_id) REFERENCES escolas(escola_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT ck_turma_nome CHECK (CHAR_LENGTH(TRIM(nome))>0),
    CONSTRAINT ck_turma_ano CHECK (ano_letivo BETWEEN 1900 AND 2100),
    CONSTRAINT ck_turma_ativo CHECK (ativo IN (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE matriculas (
    matricula_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario_id BIGINT UNSIGNED NOT NULL,
    turma_id BIGINT UNSIGNED NOT NULL,
    data_matricula DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ativa',
    UNIQUE KEY uq_matricula (usuario_id, turma_id),
    CONSTRAINT fk_matricula_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_matricula_turma FOREIGN KEY (turma_id) REFERENCES turmas(turma_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT ck_matricula_status CHECK (status IN ('ativa','concluida','cancelada','transferida'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE perfis (
    perfil_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(30) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE usuario_perfis (
    usuario_id BIGINT UNSIGNED NOT NULL,
    perfil_id SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (usuario_id, perfil_id),
    CONSTRAINT fk_usuario_perfis_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_usuario_perfis_perfil FOREIGN KEY (perfil_id) REFERENCES perfis(perfil_id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE preferencias (
    usuario_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    tema VARCHAR(10) NOT NULL DEFAULT 'claro',
    fonte VARCHAR(10) NOT NULL DEFAULT 'normal',
    CONSTRAINT fk_preferencias_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT ck_preferencias_tema CHECK (tema IN ('claro','escuro')),
    CONSTRAINT ck_preferencias_fonte CHECK (fonte IN ('normal','grande'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO perfis(nome) VALUES ('aluno'), ('professor'), ('administrador');

-- A imagem cria unifica_app para UNIFICA; limitar suas permissoes ao CRUD.
REVOKE ALL PRIVILEGES ON UNIFICA.* FROM 'unifica_app'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON UNIFICA.* TO 'unifica_app'@'%';
