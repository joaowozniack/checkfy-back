class ImplementacaoOrganizacional:
    def __init__(self, db):
        self.db = db

    def get_perguntas(self, id_nivel):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query_perguntas = "SELECT * FROM perguntas_capacidade_processo_organizacional WHERE ID_Nivel = %s"
            cursor.execute(query_perguntas, (id_nivel,))
            perguntas = cursor.fetchall()
            # Verificar se a consulta retornou algo
            if not perguntas:
                return None  # Retorna uma mensagem informando que não encontrou nada
            
            perguntas_implementacao = []
            for pergunta in perguntas:
                pergunta_dict = {
                    'ID': pergunta['ID'],
                    'pergunta': pergunta['Pergunta'],
                    'ID_Nivel': pergunta['ID_Nivel']
                }
                perguntas_implementacao.append(pergunta_dict)
            cursor.close()
            return perguntas_implementacao

        except Exception as e:
            print(f"Erro ao buscar perguntas de implementação: {e}")
            raise

    def add_capacidade_processo_organizacional(self, valores):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
        INSERT INTO nota_capacidade_processo_organizacional 
        (ID_Avaliacao, ID_Processo, Nota) 
        VALUES (%s, %s, %s)
        """
        try:
            # Executa a inserção de múltiplos valores ao mesmo tempo
            cursor.executemany(query, valores)
            self.db.conn.commit()  # Confirma a operação no banco de dados
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao adicionar os graus de implementação: {e}")
            raise
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def get_capacidade_processo_organizacional(self, id_avaliacao):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query_graus = "SELECT * FROM nota_capacidade_processo_organizacional WHERE ID_Avaliacao = %s"
            cursor.execute(query_graus, (id_avaliacao,))
            graus = cursor.fetchall()

            # Verificar se a consulta retornou algo
            if not graus:
                return None  # Retorna uma mensagem informando que não encontrou nada
            
            capacidade_processo = []
            for grau in graus:
                grau_dict = {
                    'ID': grau['ID'],
                    'ID_Processo': grau['ID_Processo'],
                    'Nota': grau['Nota'],
                    'ID_Avaliacao': grau['ID_Avaliacao'],
                }
                capacidade_processo.append(grau_dict)
            cursor.close()
            return capacidade_processo

        except Exception as e:
            print(f"Erro ao buscar graus de implementação: {e}")
            raise

    def update_capacidade_processo_organizacional_batch(self, update_data):
        cursor = self.db.conn.cursor(dictionary=True)
        query = """
            UPDATE nota_capacidade_processo_organizacional
            SET Nota = %s
            WHERE ID_Avaliacao = %s AND ID_Processo = %s
        """
        try:
            # Executa a atualização para cada item no batch de dados
            cursor.executemany(query, update_data)
            self.db.conn.commit()  # Confirma a operação no banco de dados
        except Exception as e:
            self.db.conn.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao atualizar capacidade do processo: {e}")
            raise
        finally:
            cursor.close()  # Garante que o cursor será fechado

    def get_evidencias_por_pergunta(self, pergunta_id, processo_id):
        cursor = self.db.conn.cursor(dictionary=True)
        try:
            query = """
                SELECT * FROM arquivo_capacidade_processo_organizacional
                WHERE ID_Pergunta = %s AND ID_Processo = %s
            """
            cursor.execute(query, (pergunta_id, processo_id))
            evidencias = cursor.fetchall()
            cursor.close()
            return evidencias
        except Exception as e:
            print(f"Erro ao buscar evidências: {e}")
            raise

    def add_evidencia_organizacional(self, id_pergunta, id_processo, caminho_arquivo, nome_arquivo, id_avaliacao):
        cursor = self.db.conn.cursor()
        try:
            query = """
                INSERT INTO arquivo_capacidade_processo_organizacional
                (Caminho_Arquivo, Nome_Arquivo, ID_Pergunta, ID_Processo, ID_Avaliacao)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (caminho_arquivo, nome_arquivo, id_pergunta, id_processo, id_avaliacao))
            self.db.conn.commit()
            evidencia_id = cursor.lastrowid
            cursor.close()
            return evidencia_id
        except Exception as e:
            self.db.conn.rollback()
            print(f"Erro ao adicionar evidência: {e}")
            raise

    def delete_evidencia_organizacional(self, evidencia_id):
        cursor = self.db.conn.cursor()
        try:
            query = "DELETE FROM arquivo_capacidade_processo_organizacional WHERE ID = %s"
            cursor.execute(query, (evidencia_id,))
            self.db.conn.commit()
            cursor.close()
        except Exception as e:
            self.db.conn.rollback()
            print(f"Erro ao deletar evidência: {e}")
            raise