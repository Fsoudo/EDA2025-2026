import java.util.Scanner;

public class Main {

    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        Pilha pilha = new Pilha(5);
        Fila fila = new Fila(5);
        ListaLigada lista = new ListaLigada();

        int opcao;

        do {
            mostrarMenu();
            opcao = lerInteiro("Escolhe uma opção: ");
            System.out.println();

            switch (opcao) {
                case 1:
                    int valorPush = lerInteiro("Valor para inserir na pilha: ");
                    pilha.push(valorPush);
                    pilha.mostrar();
                    break;

                case 2:
                    Integer removidoPilha = pilha.pop();
                    if (removidoPilha != null) {
                        System.out.println("Removido da pilha: " + removidoPilha);
                    }
                    pilha.mostrar();
                    break;

                case 3:
                    int valorEnqueue = lerInteiro("Valor para inserir na fila: ");
                    fila.enqueue(valorEnqueue);
                    fila.mostrar();
                    break;

                case 4:
                    Integer removidoFila = fila.dequeue();
                    if (removidoFila != null) {
                        System.out.println("Removido da fila: " + removidoFila);
                    }
                    fila.mostrar();
                    break;

                case 5:
                    int valorLista = lerInteiro("Valor para inserir na lista ligada: ");
                    lista.inserirNoInicio(valorLista);
                    lista.mostrar();
                    break;

                case 6:
                    int valorRemoverLista = lerInteiro("Valor para remover da lista ligada: ");
                    boolean removido = lista.remover(valorRemoverLista);
                    if (removido) {
                        System.out.println("Valor removido com sucesso.");
                    } else {
                        System.out.println("Valor não encontrado.");
                    }
                    lista.mostrar();
                    break;

                case 7:
                    int valorProcurar = lerInteiro("Valor a procurar na lista ligada: ");
                    boolean existe = lista.procurar(valorProcurar);
                    System.out.println("Existe " + valorProcurar + "? " + existe);
                    break;

                case 8:
                    System.out.println("Estado atual das estruturas:");
                    pilha.mostrar();
                    fila.mostrar();
                    lista.mostrar();
                    break;

                case 0:
                    System.out.println("Programa terminado.");
                    break;

                default:
                    System.out.println("Opção inválida.");
            }

            System.out.println();
        } while (opcao != 0);

        scanner.close();
    }

    static void mostrarMenu() {
        System.out.println("=== MENU ESTRUTURAS DINÂMICAS ===");
        System.out.println("1 - Push na pilha");
        System.out.println("2 - Pop da pilha");
        System.out.println("3 - Enqueue na fila");
        System.out.println("4 - Dequeue da fila");
        System.out.println("5 - Inserir na lista ligada");
        System.out.println("6 - Remover da lista ligada");
        System.out.println("7 - Procurar na lista ligada");
        System.out.println("8 - Mostrar todas as estruturas");
        System.out.println("0 - Sair");
    }

    static int lerInteiro(String mensagem) {
        while (true) {
            System.out.print(mensagem);
            if (scanner.hasNextInt()) {
                return scanner.nextInt();
            } else {
                System.out.println("Erro: tens de inserir um número inteiro.");
                scanner.next();
            }
        }
    }

    // =========================================================
    // PILHA
    // =========================================================
    static class Pilha {
        private int[] dados;
        private int topo;

        public Pilha(int capacidade) {
            dados = new int[capacidade];
            topo = -1;
        }

        public boolean estaVazia() {
            return topo == -1;
        }

        public boolean estaCheia() {
            return topo == dados.length - 1;
        }

        public void push(int valor) {
            if (estaCheia()) {
                System.out.println("Erro: overflow na pilha.");
                return;
            }
            topo++;
            dados[topo] = valor;
            System.out.println("Valor inserido na pilha.");
        }

        public Integer pop() {
            if (estaVazia()) {
                System.out.println("Erro: underflow na pilha.");
                return null;
            }
            int valor = dados[topo];
            topo--;
            return valor;
        }

        public void mostrar() {
            System.out.print("Pilha: [");
            for (int i = 0; i <= topo; i++) {
                System.out.print(dados[i]);
                if (i < topo) {
                    System.out.print(", ");
                }
            }
            System.out.println("]");
        }
    }

    // =========================================================
    // FILA
    // =========================================================
    static class Fila {
        private int[] dados;
        private int head;
        private int tail;
        private int tamanho;

        public Fila(int capacidade) {
            dados = new int[capacidade];
            head = 0;
            tail = 0;
            tamanho = 0;
        }

        public boolean estaVazia() {
            return tamanho == 0;
        }

        public boolean estaCheia() {
            return tamanho == dados.length;
        }

        public void enqueue(int valor) {
            if (estaCheia()) {
                System.out.println("Erro: overflow na fila.");
                return;
            }
            dados[tail] = valor;
            tail = (tail + 1) % dados.length;
            tamanho++;
            System.out.println("Valor inserido na fila.");
        }

        public Integer dequeue() {
            if (estaVazia()) {
                System.out.println("Erro: underflow na fila.");
                return null;
            }
            int valor = dados[head];
            head = (head + 1) % dados.length;
            tamanho--;
            return valor;
        }

        public void mostrar() {
            System.out.print("Fila: [");
            for (int i = 0; i < tamanho; i++) {
                int indice = (head + i) % dados.length;
                System.out.print(dados[indice]);
                if (i < tamanho - 1) {
                    System.out.print(", ");
                }
            }
            System.out.println("]");
        }
    }

    // =========================================================
    // LISTA LIGADA
    // =========================================================
    static class No {
        int valor;
        No next;

        No(int valor) {
            this.valor = valor;
        }
    }

    static class ListaLigada {
        private No head;

        public void inserirNoInicio(int valor) {
            No novo = new No(valor);
            novo.next = head;
            head = novo;
            System.out.println("Valor inserido na lista ligada.");
        }

        public boolean procurar(int valor) {
            No atual = head;
            while (atual != null) {
                if (atual.valor == valor) {
                    return true;
                }
                atual = atual.next;
            }
            return false;
        }

        public boolean remover(int valor) {
            if (head == null) {
                return false;
            }

            if (head.valor == valor) {
                head = head.next;
                return true;
            }

            No atual = head;
            while (atual.next != null) {
                if (atual.next.valor == valor) {
                    atual.next = atual.next.next;
                    return true;
                }
                atual = atual.next;
            }

            return false;
        }

        public void mostrar() {
            System.out.print("Lista ligada: ");
            No atual = head;

            if (atual == null) {
                System.out.println("null");
                return;
            }

            while (atual != null) {
                System.out.print(atual.valor + " -> ");
                atual = atual.next;
            }
            System.out.println("null");
        }
    }
}