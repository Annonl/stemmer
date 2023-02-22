class Stemmer:
    VOWELS = "аеиоуюя"
    
    PERFECTIVE_GERUND_GROUP_1 = ["в", "вши", "вшись"]
    PERFECTIVE_GERUND_GROUP_2 = ["ив", "ивши", "ившись", "ыв", "ывши", "ывшись"]

    ADJECTIVE = ["ее", "ие", "ые", "ое", "ими", "ыми", "ей", "ий", "ый", "ой", "ем", "им", "ым", "ом", "его", "ого", "ему", "ому", "их", "ых", "ую", "юю", "ая", "яя", "ою", "ею"]

    PARTICIPLE_GROUP_1 = ["ем", "нн", "вш", "ющ", "щ"]
    PARTICIPLE_GROUP_2 = ["ивш", "ывш", "ующ"]

    REFLEXIVE = ["ся", "сь"]

    VERB_GROUP_1 = ["ла", "на", "ете", "йте", "ли", "й", "л", "ем", "н", "ло", "но", "ет", "ют", "ны", "ть", "ешь", "нно"]
    VERB_GROUP_2 = ["ила", "ыла", "ена", "ейте", "уйте", "ите", "или", "ыли", "ей", "уй", "ил", "ыл", "им", "ым", "ен", "ило", "ыло", "ено", "ят", "ует", "уют", "ит", "ыт", "ены", "ить", "ыть", "ишь", "ую", "ю"]

    NOUN = ["а", "ев", "ов", "ие", "ье", "е", "иями", "ями", "ами", "еи", "ии", "и", "ией", "ей", "ой", "ий", "й", "иям", "ям", "ием", "ем", "ам", "ом", "о","у", "ах", "иях", "ях", "ы", "ь", "ию", "ью", "ю", "ия", "ья", "я"]

    SUPERLATIVE = ["ейш", "ейше"]
    DERIVATIONAL = ["ост", "ость"]


    def get_base(self, word: str):
        word = word.lower()
        
        first = self.__find_ending(self.__get_RV(word), self.PERFECTIVE_GERUND_GROUP_1, ["а", "я"])
        if first == None:
            first = self.__find_ending(word, self.PERFECTIVE_GERUND_GROUP_2)
        
        if first == None:  
            first = self.__find_ending(word, self.REFLEXIVE)
            if first != None:
                word = self.__delete_ending(word, self.__get_len(first))
            
            word = self.__delete_adj_verb_noun(word)


        else:
            word = self.__delete_ending(word, self.__get_len(first))

        second = self.__find_ending(self.__get_RV(word), ["и"])
        if second != None:
            word = self.__delete_ending(word, 1)
        
        third = self.__find_ending(self.__get_RN(word, 2), self.DERIVATIONAL)

        if third != None:
            word = self.__delete_ending(word, self.__get_len(third))

        four = self.__find_ending(word, ["ь"])
        if four != None:
            word = self.__delete_ending(word, 1)
        else:
            word = self.__find_and_delete(word, self.SUPERLATIVE)
            
            four = self.__find_ending(word, ["нн"])
            if four != None:
                word = self.__delete_ending(word, 1)

                
        return word


    def __delete_adj_verb_noun(self, word):
        first = self.__find_ending(self.__get_RV(word), self.__get_adjective_participle(self.ADJECTIVE, self.PARTICIPLE_GROUP_1), ["а", "я"])
        if first != None:
            return self.__delete_ending(word, self.__get_len(first))
        else:
            first = self.__find_ending(self.__get_RV(word), self.__get_adjective_participle(self.ADJECTIVE, self.PARTICIPLE_GROUP_2))
            if first != None:
                return self.__delete_ending(word, self.__get_len(first))
            first = self.__find_ending(self.__get_RV(word), self.ADJECTIVE)
            if first != None:
                return self.__delete_ending(word, self.__get_len(first))
            
        first = self.__find_ending(self.__get_RV(word), self.VERB_GROUP_1, ["а", "я"])

        if first != None:
            return self.__delete_ending(word, self.__get_len(first))
        else:
            first = self.__find_ending(self.__get_RV(word), self.VERB_GROUP_2)
            if first != None:
                return self.__delete_ending(word, self.__get_len(first))
        

        word = self.__find_and_delete(word, self.NOUN)
        return word

    def __find_and_delete(self, word, arr, prev = []):
        temp_word = self.__get_RV(word)
        if prev != []:
            temp_word = self.__get_RV(word)
        res = self.__find_ending(temp_word, arr, prev)
        if res != None:
            return self.__delete_ending(word, self.__get_len(res))
        return word

    def __get_adjective_participle(self, adj, part):
        result = []
        for i in part:
            for j in adj:
                result.append(i + j)
        return result

    def __get_len(self, arr) -> int:
        return len(max(arr, key=len))

    def __get_RV(self, word: str) -> str:
        min_index = len(word) + 1
        for c in self.VOWELS:
            i = word.find(c.__str__())
            if i < min_index and i != -1:
                min_index = i
        return word[min_index + 1:]

    def __find_ending(self, word: str, endings: list[str], previous = []):
        result = []
        for ending in endings:
            if word.endswith(ending):
                if len(previous) == 0:
                    result.append(ending)
                for pre in previous:
                    if word[-len(ending)] == pre:
                        result.append(ending)
        if len(result) == 0:
            return None
        return result
    
    def __delete_ending(self, word: str, len_ending: int) -> str:
        return word[:-len_ending]

    def __get_RN(self, word: str, n = 1) -> str:
        flag = False
        index = -1
        for i in range(len(word)):
            if flag and self.VOWELS.find(word[i]) == -1:
                index = i + 1
                break
            flag = self.VOWELS.find(word[i]) != -1

        if n != 1:
            return self.__get_RN(word[index:], n - 1)
        return word[index:]

