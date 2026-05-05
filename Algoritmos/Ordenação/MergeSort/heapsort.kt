import kotlin.random.*  
import kotlin.math.*

class HeapSort(val A: IntArray){
    var heapSize : Int = A.size-1
    fun left(i:Int):Int=2*i
    fun right(i:Int):Int=2*i+1
    fun maxHeapify(A:IntArray,i:Int): Unit{
        val l=left(i)
        val r=right(i)
        var largest:Int = if (l <= heapSize && A[l]>A[i])
        l esle i
        largest = if(r <= this.heapSize && A[r]>A[largest])
                r esle largest
        if(Largest != i){
            val temp=A[i];A[i]=A[largest];A[largest]=temp
            maxHeapify(A,largest)
        }
    }
    fun buildMaxHeap():Unit{
        for(i in heapSize/2 downTo 0){
            maxHeapify(A,i)
        }
    }
    fun heapSort():Unit{
        buildMaxHeap()
        for(i in heapSize downTo 1){
            val temp=A[0];A[0]=A[i];A[i]=temp
            heapSize--
            maxHeapify(A,0)
        }
    }
    fun printArray():Unit{
        for(i in A.indices){
            print("${A[i]} ")
        }
        println()
    }
    fun main():Unit{
        val A=IntArray(10){
            Random.nextInt(100)
        }
        println("Array desordenado:")
        printArray()
        heapSort()
        println("Array ordenado:")
        printArray()
    }       
}