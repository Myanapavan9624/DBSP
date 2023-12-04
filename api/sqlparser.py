import sqlparse
import collections 
import re
from operator import mul, add, sub, truediv
from custom_errors import *

FROM = "FROM"
SELECT = "SELECT"
GROUP_BY = "GROUP BY"
ORDER_BY = "ORDER BY"
range_comparators = {"<=", ">=", ">", "<"}
operators = {"<", "=", ">", "!"}

class SQLParser:
    def __init__(self):
        self.comparison = collections.defaultdict(list)
        self.parenthesis = list()
        self.select_attributes = list()
        self.tables = list()
        self.orderby_attributes = list()
        self.groupby_attributes = list()

    # def clean_query(self, sql):
    #     try:
    #         # date
    #         sql = sql.replace(" date ", " ")


    #         start = self.query_index("+ interval", sql)
    #         if start != -1:
    #             end = sql.find('\n', start)
    #             if end != -1:
    #                 sql = sql[:start] + sql[end:]
    #             else:
    #                 sql = sql[:start]

    #         # between and calculate
    #         while self.query_index("between", sql) != -1:
    #             between_start = self.query_index("between", sql)
    #             between_end = between_start + len("between")
    #             if sql[between_end + 1].isnumeric():  # between a number to number
    #                 i = between_end + 1
    #                 calc_end = 0
    #                 while sql[i].lower() != "a":
    #                     calc_end = i - 1
    #                     i += 1
    #                 first_expression = sql[between_end + 1 : calc_end + 1].strip()

    #                 while not sql[i].isnumeric():
    #                     second_calc_start = i
    #                     i += 1

    #                 while ord(sql[i]) != 10:
    #                     second_calc_end = i
    #                     i += 1

    #                 second_expression = sql[second_calc_start + 1 : second_calc_end + 1]
    #                 sql = (
    #                     sql[: between_end + 1]
    #                     + "{}".format(self.calculate(first_expression))
    #                     + sql[calc_end + 1 : second_calc_start + 1]
    #                     + "{}".format(self.calculate(second_expression))
    #                     + sql[second_calc_end + 1 :]
    #                 )

    #             start = 0
    #             for i in range(between_start - 2, -1, -1):
    #                 if ord(sql[i]) == 32:
    #                     start = i + 1
    #                     break
    #             predicate_to_add = sql[start : between_start - 1]
    #             rest = sql[between_end + 1 :]
    #             and_start = self.query_index("and", rest)
    #             sql = (
    #                 sql[:between_start]
    #                 + ">= "
    #                 + rest[: and_start + 3]
    #                 + " {} <=".format(predicate_to_add)
    #                 + rest[and_start + 3 :]
    #             )

    #         sql = sql.replace("\t", "").replace("\n", " ")
    #         return sql
    #     except CustomError as e:
    #         raise CustomError(str(e))
    #     except:
    #         raise CustomError("Error in clean_query() - Unable to clean the SQL query.")

    def parse_query(self, sql):
        try:
            nested_sql_ = self.nested_query(sql)
            # nested_sql = self.remove_double_spacing(nested_sql_)
            nested_sql = nested_sql_.replace('  ', '')
            formatted_sql = self.sql_formatter(nested_sql)
            # cleaned_sql = self.clean_query(formatted_sql)
            parsed = sqlparse.parse(formatted_sql)
            stmt = parsed[0]
            from_seen, select_seen, where_seen, groupby_seen, orderby_seen = (
                False,
                False,
                False,
                False,
                False,
            )


            def append_identifiers_if_seen(self, token, attribute_list):
                if isinstance(token, sqlparse.sql.IdentifierList):
                    attribute_list.extend(token.get_identifiers())
                elif isinstance(token, sqlparse.sql.Identifier):
                    attribute_list.append(token)

            for token in stmt.tokens:
                # Append identifiers to respective lists based on seen flags
                if select_seen:
                    append_identifiers_if_seen(self, token, self.select_attributes)
                if from_seen:
                    append_identifiers_if_seen(self, token, self.tables)
                if orderby_seen:
                    append_identifiers_if_seen(self, token, self.orderby_attributes)
                if groupby_seen:
                     append_identifiers_if_seen(self, token, self.groupby_attributes)

                if isinstance(token, sqlparse.sql.Where):
                    select_seen, from_seen, where_seen, groupby_seen, orderby_seen = False, False, True, False, False
                    # select_seen = False
                    # from_seen = False
                    # where_seen = True
                    # groupby_seen = False
                    # orderby_seen = False
                    for tokens in token:
                        if isinstance(tokens, sqlparse.sql.Comparison):
                            comparison_string = f"{tokens}\n"
                            comparison_key, comparison_operator, comparison_value = map(str.strip, comparison_string.split(" "))
                            self.comparison[comparison_key].append((comparison_operator, comparison_value))
                        # Check if it's a parenthesis expression
                        elif isinstance(tokens, sqlparse.sql.Parenthesis):
                            parenthesis_string = f"{tokens}\n"
                            self.parenthesis.append(parenthesis_string)
                        # if isinstance(where_tokens, sqlparse.sql.Comparison):
                        #     comparison_string = "{}\n".format(where_tokens)
                        #     (
                        #         comparison_key,
                        #         comparison_operator,
                        #         comparison_value,
                        #     ) = comparison_string.strip().split(" ")
                        #     self.comparison[comparison_key].append(
                        #         (comparison_operator, comparison_value)
                        #     )
                        # elif isinstance(where_tokens, sqlparse.sql.Parenthesis):
                        #     parenthesis_string = "{}\n".format(where_tokens)
                        #     self.parenthesis.append(parenthesis_string)

            keyword_mappings = {
                GROUP_BY: (False, False, False, True, False),
                ORDER_BY: (False, False, False, False, True),
                FROM: (False, True, False, False, False),
                SELECT: (True, False, False, False, False)
            }

            # Check if the token is a keyword and update seen flags accordingly
            if token.ttype is sqlparse.tokens.Keyword:
                keyword_upper = token.value.upper()
                select_seen, from_seen, where_seen, groupby_seen, orderby_seen = keyword_mappings.get(keyword_upper, (False, False, False, False, False))

            # if (
            #     token.ttype is sqlparse.tokens.Keyword
            #     and token.value.upper() == GROUP_BY
            # ):
            #     select_seen = False
            #     from_seen = False
            #     where_seen = False
            #     groupby_seen = True
            #     orderby_seen = False
            # if (
            #     token.ttype is sqlparse.tokens.Keyword
            #     and token.value.upper() == ORDER_BY
            # ):
            #     select_seen = False
            #     from_seen = False
            #     where_seen = False
            #     groupby_seen = False
            #     orderby_seen = True
            # if token.ttype is sqlparse.tokens.Keyword and token.value.upper() == FROM:
            #     select_seen = False
            #     from_seen = True
            #     where_seen = False
            #     groupby_seen = False
            #     orderby_seen = False
            # if token.ttype is sqlparse.tokens.DML and token.value.upper() == SELECT:
            #     select_seen = True
            #     from_seen = False
            #     where_seen = False
            #     groupby_seen = False
            #     orderby_seen = False
        except CustomError as e:
            raise CustomError(str(e))
        except:
            raise CustomError("Error in parse_query() - Unable to parse the SQL query.")

    def query_index(self, inside, whole):
        if(whole.find(inside)>=0):
            return whole.find(inside);
        return -1;

    def calculate(self, s):
        try:
            OP = {"*": mul, "+": add, "-": sub, "/": truediv}
            # op_set = {"+", "*", "-", "/"}
            cur_op = ""
            cur_num, prev_num = "", ""
            num_chars = [char for char in s if char != ""]
            for char in num_chars:
                if char in OP.keys():
                    cur_op, prev_num, cur_num = char, cur_num, ""
                elif char != " ":
                    cur_num += char
            return OP[cur_op](float(prev_num), float(cur_num))
        except CustomError as e:
            raise CustomError(str(e))
        except:
            raise CustomError(
                "Error in calculate() - Unable to calculate attribute value."
            )

    def sql_formatter(self, sql):
        try:
            # Define the set of operators
            operators_set = set(['=', '<', '>', '!', '+', '-', '*', '/', '%', '^', '&', '|', '~'])
            
            # Use regular expression to add spaces around the operators
            formatted_sql = re.sub(f"([{re.escape(''.join(operators_set))}])", r" \1 ", sql)

            # Replace multiple spaces with a single space
            formatted_sql = re.sub(r'\s+', ' ', formatted_sql).strip()

            return formatted_sql
        except CustomError as e:
            raise CustomError(str(e))
        except Exception as e:
            raise CustomError(f"Error in sql_formatter() - {e}")
        # try:
        #   end = 0 
        #   temp = ""
        #   for index in range(1, len(sql)-1): 
        #       if sql[index] in operators: 
        #           if sql[index-1] not in operators and ord(sql[index-1]) != 32: 
        #               temp += sql[end: index] + ' ' 
        #               end = index
        #           if sql[index+1] not in operators and ord(sql[index+1]) != 32: 
        #               temp += sql[end: index+1] + ' '
        #               end = index + 1 

        #   temp += sql[end: len(sql)]
        #   return temp
        # except CustomError as e:
        #     raise CustomError(str(e))
        # except:
        #     raise CustomError(
        #         "Error in sql_formatter() - Unable to format the SQL statement."
        #     )
        

    def nested_query(self, sql): 
        try:
            select_index = list()
            splitted_word_sql = sql.split(" ")
            
            for i, word in enumerate(splitted_word_sql): 
                # if word == 'select\n' or word =='SELECT\n':
                #     select_index.append(i)
                if word in ['select\n', 'SELECT\n']:
                    select_index.append(i)
            if len(select_index) == 2: 
                # start_index = int(select_index[1])
                # end_index = int(select_index[1])
                start_index = end_index = int(select_index[1])
                while not splitted_word_sql[start_index].startswith('('):
                    start_index -= 1  
                flag = False
                for i in range(start_index, start_index-3, -1): 
                    if splitted_word_sql[i] in range_comparators:
                        flag = True
                        break;
                if flag:
                    # start_part = splitted_word_sql[start_index][2:] 
                    # if len(splitted_word_sql[start_index]) > 1 else splitted_word_sql[start_index]
                    if len(splitted_word_sql[start_index]) > 1:
                        start_part = splitted_word_sql[start_index][2:]
                    else:
                        start_part = splitted_word_sql[start_index]

                    while not splitted_word_sql[end_index].startswith(')'): 
                        end_index += 1
                    # end_part = splitted_word_sql[end_index][1:] \
                    # if len(splitted_word_sql[end_index]) > 1 else splitted_word_sql[end_index]
                    if len(splitted_word_sql[end_index]) > 1:
                        end_part = splitted_word_sql[end_index][1:]
                    else:
                        end_part = splitted_word_sql[end_index]
                    
                    # Extract parts of the string before, at, and after the indices
                    before_start_index = " ".join(splitted_word_sql[:start_index])
                    after_end_index = " ".join(splitted_word_sql[end_index + 1:])

                    # Construct the final string
                    final_string = before_start_index + " " + start_part + " 100 " + end_part + " " + after_end_index

                    return final_string.strip()


                    # return " ".join(splitted_word_sql[:start_index] + [start_part]+ ['100'] + [end_part]+splitted_word_sql[end_index+1:])
            return sql
        except CustomError as e:
            raise CustomError(str(e))
        except:
            raise CustomError("Error in nested_query() - Unable to parse the nested query. Have mercy and give us something less nested please.")
