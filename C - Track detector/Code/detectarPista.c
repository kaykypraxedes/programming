/* detectarPista.c */
/*
Desenvolvedores:
    Kayky Moreira Praxedes
    Carlos Ernesto Cardoso dos Reis
*/

#include <stdio.h>
#include <stdlib.h>

typedef struct LIST{
    int key;
    int type;
    int element_count;
    struct LIST *next;
} LIST;
/*
Cria o tipo LISTPTR para evitar de usar ponteiro duplo **
(mais confortável visualmente)
*/
typedef LIST *LISTPTR;

// CreateNode: aloca e inicializa um nó da lista
void CreateNode(LISTPTR *list, int key, int type){
    *list = (LISTPTR)malloc(sizeof(LIST));
    (*list)->key = key;
    (*list)->type = type;
    (*list)->element_count = 1;
    (*list)->next = NULL;
}

// FindKeyType: busca key na lista; retorna ultimo no e preenche *type se encontrada
LISTPTR FindKeyType(LISTPTR list, int key, int *type){
    LISTPTR last = NULL;
    while(list != NULL){
        if(list->key == key) *type = list->type;
        last = list;
        list = list->next;
    }
    return last;
}

// AppendNode: cria no e anexa apos previous, retorna o novo no
LISTPTR AppendNode(LISTPTR previous, int key, int type){
    LISTPTR new_node;
    CreateNode(&new_node, key, type);
    previous->next = new_node;
    return new_node;
}

// ReclassifyByKey: reajusta types apos insercao de chave nova
void ReclassifyByKey(LISTPTR list, LISTPTR new_node){
    int max_key = -1;
    while(list != NULL){
        if(new_node->key < list->key)
            list->type++;
        else if(new_node->key > list->key && list->key > max_key){
            new_node->type = list->type + 1;
            max_key = list->key;
        }
        list = list->next;
    }
}

// InsertKey: insere chave na lista encadeada
void InsertKey(LISTPTR *list, int key){
    int repeated_type = 0;
    LISTPTR last = FindKeyType(*list, key, &repeated_type);
    if(!last) return;

    if(last->key == key){
        last->element_count++;
    } else {
        LISTPTR new_node = AppendNode(last, key, repeated_type ? repeated_type : 1);
        if(!repeated_type)
            ReclassifyByKey(*list, new_node);
    }
}

// MatchPattern5: tenta casar 5 tipos consecutivos e calcula contribuicao do midpoint
int MatchPattern5(LISTPTR start, int pattern[5], int *midpoint_sum){
    LISTPTR nodes[5];
    for(int i = 0; i < 5; i++){
        if(start == NULL || start->type != pattern[i])
            return 0;
        nodes[i] = start;
        start = start->next;
    }
    *midpoint_sum = nodes[0]->element_count
                  + nodes[1]->element_count
                  + nodes[2]->element_count / 2;
    return 1;
}

// FindSubPattern: tenta casar pattern[0..len-1] a partir de start
// Retorna o ultimo no casado, ou NULL se nao casar
LISTPTR FindSubPattern(LISTPTR start, int pattern[], int len){
    LISTPTR last = NULL;
    for(int i = 0; i < len; i++){
        if(start == NULL || start->type != pattern[i])
            return NULL;
        last = start;
        start = start->next;
    }
    return last;
}

// FindLane: busca padrao (1,3,2,3,1) e retorna ponto medio
int FindLane(LISTPTR list){
    int pattern[5] = {1, 3, 2, 3, 1};
    int accumulated = 0;
    while(list != NULL){
        int midpoint_contrib;
        if(MatchPattern5(list, pattern, &midpoint_contrib))
            return accumulated + midpoint_contrib;
        accumulated += list->element_count;
        list = list->next;
    }
    return -1;
}

// CheckObstacle: detecta padroes de obstaculo na pista
int CheckObstacle(LISTPTR list){
    int base_pattern[5] = {1, 3, 2, 3, 1};
    int prefix_pattern[3] = {1, 3, 2};
    int close_pattern[2] = {3, 1};
    while(list != NULL){
        if(FindSubPattern(list, base_pattern, 5) != NULL)
            return 0;
        LISTPTR after_prefix = FindSubPattern(list, prefix_pattern, 3);
        if(after_prefix != NULL){
            LISTPTR scan = after_prefix->next;
            while(scan != NULL){
                if(FindSubPattern(scan, close_pattern, 2) != NULL)
                    return 1;
                scan = scan->next;
            }
        }
        list = list->next;
    }
    return -1;
}

// CountObstacles: conta valores == 1 no vetor
int CountObstacles(int array[], int size){
    int counter = 0;
    for(int i = 0; i < size; i++){
        if(array[i]==1){
            counter++;
        }
    }
    return counter;
}

// FreeList: percorre e desaloca todos os nos
void FreeList(LISTPTR *list){
    LISTPTR current = NULL;
    while(*list != NULL){
        current = *list;
        *list = (*list)->next;
        free(current);
    }
}

int main(){
    LISTPTR my_list = NULL;
    int row_len, L;
    if (scanf(" %d", &L) != 1) return 1;
    int *midpoints = malloc(L * sizeof(int));
    int *obstacles = malloc(L * sizeof(int));
    if (!midpoints || !obstacles) { free(midpoints); free(obstacles); return 1; }
    int midpoint = 0, obstacle = 0, obs_count = 0;
    for(int i = 0; i < L; i++){
        if (scanf(" %d", &row_len) != 1){ FreeList(&my_list); return 1; }
        for(int j = 0; j < row_len; j++){
            int key;
            if (scanf(" %d", &key) != 1){ FreeList(&my_list); return 1; }
            if(j == 0) CreateNode(&my_list, key, 1);
            else InsertKey(&my_list, key);
        }
        midpoint = FindLane(my_list);
        obstacle = CheckObstacle(my_list);
        FreeList(&my_list);
        midpoints[i] = midpoint;
        obstacles[i] = obstacle;
    }
    obs_count = CountObstacles(obstacles, L);
    // Calcular a media dos pontos medios
    int sum = 0, valid_count = 0, last_valid_idx=0;
    for(int i = 0; i < L; i++){
        if(midpoints[i] > 0){
            sum += midpoints[i];
            valid_count++;
            last_valid_idx = i;
        }
    }
    int mean = 0;
    // Se a quantidade de pontos medios validos for maior que 70% do total
    if (valid_count > 70 * L / 100){
        mean = (int) (sum / valid_count);
        int found = 0;
        if(mean + 14 > midpoints[last_valid_idx] && mean - 14 < midpoints[last_valid_idx]){
            printf("Pista em linha reta e ");
            found = 1;
        } else if(mean + 15 > midpoints[last_valid_idx] && midpoints[last_valid_idx] < midpoints[0]){
            printf("Curva a direita e ");
            found = 1;
        } else if(mean-15 < midpoints[last_valid_idx] && midpoints[last_valid_idx] > midpoints[0]){
            printf("Curva a esquerda e ");
            found = 1;
        }
        if(found){
            if(obs_count > 0){
                printf("com impedimento.\n");
            } else{
                printf("sem impedimento.\n");
            }
        }
    } else printf("Formato da pista não estimado.\n");
    return 0;
}
