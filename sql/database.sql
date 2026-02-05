-- =============================================
-- BASE DE DATOS: INSIDE EARTH - ESTRUCTURA DE PROYECTOS
-- =============================================

-- 1. TABLA PADRE: GEO_ADMIN_MASTER
-- Datos estáticos. Un lugar existe independientemente del negocio.
CREATE TABLE GEO_ADMIN_MASTER (
    Geo_ID INT IDENTITY(1,1) PRIMARY KEY, -- ID Autoincremental
    County_Name VARCHAR(100) NOT NULL,
    State_Province VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Region_Geografica VARCHAR(100)        -- Ej: "Cuenca del Noroeste"
);

-- 2. TABLA FILTRO: COUNTY_SCREENING
-- Primera evaluación. Relación 1 a 1 (o 1 a N historico) con Geo_ID.
CREATE TABLE COUNTY_SCREENING (
    Screening_ID INT IDENTITY(1,1) PRIMARY KEY,
    Geo_ID INT NOT NULL,
    
    -- Métricas (Usamos DECIMAL para precisión matemática, no FLOAT)
    Metric_MAIN_Infrastructure DECIMAL(5,2), -- Puntaje 0.00 a 10.00
    Metric_MAIN_Political DECIMAL(5,2),      -- Puntaje 0.00 a 10.00
    
    Score_Ponderado_MAIN DECIMAL(5,2),       -- Resultado del cálculo
    Estado_Aprobacion BIT DEFAULT 0,         -- 1 = Aprobado, 0 = Rechazado (Boolean en SQL es BIT)

    -- Conexión con el padre
    CONSTRAINT FK_Screening_Geo FOREIGN KEY (Geo_ID) 
    REFERENCES GEO_ADMIN_MASTER(Geo_ID)
);

-- 3. TABLA ZOOM IN: PREFERENTIAL_DATA
-- Datos caros. Solo existen si Estado_Aprobacion fue 1.
CREATE TABLE PREFERENTIAL_DATA (
    Data_ID INT IDENTITY(1,1) PRIMARY KEY,
    Geo_ID INT NOT NULL,
    
    Metric_PREF_Subsurface DECIMAL(10,4),    -- Alta precisión para datos geológicos
    Metric_PREF_Mineral_Index DECIMAL(10,4), 
    
    CONSTRAINT FK_PrefData_Geo FOREIGN KEY (Geo_ID) 
    REFERENCES GEO_ADMIN_MASTER(Geo_ID)
);

-- 4. TABLA EJECUCIÓN: PROJECT_MASTER
-- Aquí nace la relación 1 a N. Un Geo_ID puede tener múltiples proyectos.
CREATE TABLE PROJECT_MASTER (
    Project_ID INT IDENTITY(1,1) PRIMARY KEY,
    Geo_ID INT NOT NULL, -- Tu puntero geográfico
    
    Target_Resource VARCHAR(50) NOT NULL,    -- Ej: "Litio", "Geotermia"
    Tech_Stack_Used VARCHAR(100),            -- Ej: "Direct Lithium Extraction (DLE)"
    Status_Proyecto VARCHAR(20) DEFAULT 'Planning',
    
    CONSTRAINT FK_Project_Geo FOREIGN KEY (Geo_ID) 
    REFERENCES GEO_ADMIN_MASTER(Geo_ID)
);

-- 5. TABLA DECISIÓN: INVESTMENT_MODEL_OUTPUT
-- Resultado final del modelo financiero/riesgo.
CREATE TABLE INVESTMENT_MODEL_OUTPUT (
    Model_Run_ID INT IDENTITY(1,1) PRIMARY KEY,
    Project_ID INT NOT NULL, -- OBLIGATORIO: Se une al PROYECTO, no solo al lugar
    
    Fecha_Calculo DATETIME DEFAULT GETDATE(),
    
    Probability_Success_Weighted DECIMAL(5,2), -- Ej: 85.50 %
    Estimated_ROI DECIMAL(10,2),               -- Porcentaje de retorno
    Decision_Flag VARCHAR(10) CHECK (Decision_Flag IN ('GO', 'NO-GO', 'HOLD')), -- Restricción de valores válidos
    
    CONSTRAINT FK_Output_Project FOREIGN KEY (Project_ID) 
    REFERENCES PROJECT_MASTER(Project_ID)
);