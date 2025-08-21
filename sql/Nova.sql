CREATE DATABASE NovaDB
GO

USE NovaDB
GO

CREATE TABLE dbo.PianoDiSpedizione (
    OrdineEvolution varchar(255) NOT NULL,
    RiferimentoOrdineCliente varchar(255),
    Cliente varchar(255),
    Articolo varchar(255),
	Descrizione varchar(255),
	NotaCommerciale varchar(255),
	NotaTecnica varchar(255),
	QtaResidua float,
	PianoDiSpedizione varchar(255),
	CONSTRAINT PK_PianoDiSpedizione_OrdineEvolution PRIMARY KEY CLUSTERED (OrdineEvolution)
);

CREATE INDEX IDX_PianoDiSpedizione
ON dbo.PianoDiSpedizione (PianoDiSpedizione);

GO

DECLARE @i INT = 1;
DECLARE @p INT = 1;

WHILE @i <= 100
BEGIN
    INSERT INTO [dbo].[PianoDiSpedizione]
           ([OrdineEvolution]
           ,[RiferimentoOrdineCliente]
           ,[Cliente]
           ,[Articolo]
           ,[Descrizione]
           ,[NotaCommerciale]
           ,[NotaTecnica]
           ,[QtaResidua]
           ,[PianoDiSpedizione])
     VALUES
           (FORMAT(20250000000000 + @i, '00000000000000')
           ,FORMAT(@i, 'ORD000000')
           ,'Cliente ' + CAST(@i AS VARCHAR)
           ,'Articolo ' + FORMAT(@i, '0000')
           ,'Descrizione articolo modello ' + FORMAT(@i, '0000')
           ,CASE WHEN @i % 2 = 0 THEN 'Consegna urgente' ELSE '' END
           ,CASE WHEN @i % 5 = 0 THEN 'Montaggio richiesto' ELSE '' END
           ,100 + @i
           ,'PDS' + FORMAT(@p, '0000000000000')
           );

    SET @i = @i + 1;
	IF @i = 20 
		SET @p = @p+1
	ELSE IF @i = 40 
		SET @p = @p+1
	ELSE IF @i = 80 
		SET @p = @p+1
END