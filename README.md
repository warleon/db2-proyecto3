# Proyecto 3 de Base de datos 2.

## **Integrantes**
* Chahua, Luis
* Aguilar, Anthony
* Rubio, Ignacio
* Ángeles, Jean

# Implementación

# Backend
## Librerías utilizadas
Para este proyecto se utilizó principalmente la librería de Face Recognition. Esto nos facilitó en poder representar a las imágenes mediante vectores numéricos. Además, es la base para poder determinar el grado de similitud entre dos imágenes. Cabe resaltar que este vector tiene dimensión de tamaño 128 y será utilizado en los 3 algoritmos de este proyecto. Asimismo, se utilizaron librerías complementarias como el Rtree, que, junto con la indexación, nose permitirá obtener las k imágenes más parecidas de forma eficiente usando KNN-RTree. Por último, se usó la librería de sklearn para trabajar con el KDTree de manera eficiente.

## Análisis de la maldición de la dimensionalidad
Debido a que el tamaño de los vectores son de 128, es muy probable que, al momento de calcular las distancias entre imágenes, se pueda apreciar que hay muy poca variabilidad entre ellas, lo cual no es nada favorable si se quiere justamente analizar diferencias. Es por ello que es necesario hacer una reducción de la dimensionalidad.
<img src="src/imagen1.png" width="800">

Se puede apreciar en este gráfico que a mayor tamaño de la dimensionalidad, hay menor variabilidad en las distancias. Asimismo, también influye mucho la cantidad de información que se puede almacenar en una estructura. Por ejemplo, para el KDTree, como cada vector se almacena en un árbol, cada nodo tendrá que almacenar una grán cantidad de datos, lo cual puede afecta en la cantidad de memoria y en el costo de las búsquedas.
Para mitigar esto, se utilizó el módulo PCA proporcionado por la librería de SKLearn. Esto te permite reducir la dimensionalidad de la imagen. Para este caso, se redució hasta 50, note que no puede ser tan pequeño porque se puede perder información importante de las imágenes. 

## Experimentación 

La experimentación se realizó variando los tamaños de N y fijando el valor de k=8. Además, calcularemos los tiempos en cada algoritmo mediante la función experimentacion definida en el código(para KDTree, KNN_Sequential) y se ejecutar á la función de KRtree para calcular su tiempo. Primero, de forma teórica, se sabe que para el KNNSecuencial, la complejidad es de O(N*D + N*logk) donde D representa a la complejidad del cálculo de la distancia entre 2 imágenes. Los resultados han sido los siguientes:

<table>
    <thead>
        <tr>
            <th></th>
            <th >K = 8</th>
            <th></th>
        </tr>
        <tr>
            <th></th>
            <th>KNN Secuencial</th>
            <th>KNN RTree</th>
            <th>KNN HighD</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td >N = 100</td>
            <td >0.0002</td>
            <td> </td>
            <td>0.00011075</td>
        </tr>
        <tr>
            <td>N = 200</td>
            <td >0.0004</td>
            <td> </td>
            <td>0.00016875</td>
        </tr>
        <tr>
            <td >N = 400</td>
            <td>0.0008</td>
            <td> </td>
            <td>0.00020075</td>
        </tr>
        <tr>
            <td>N = 800</td>
            <td>0.0022</td>
            <td> </td>
            <td>0.0003375</td>
        </tr>
        <tr>
            <td>N = 1600</td>
            <td>0.00492</td>
            <td> </td>
            <td>0.0005102500000000001</td>
        </tr>
        <tr>
            <td>N = 3200</td>
            <td>0.0071</td>
            <td> </td>
            <td>0.00087975</td>
        </tr>
        <tr>
            <td>N = 6400</td>
            <td>0.01453</td>
            <td> </td>
            <td>0.0010344999999999998</td>
        </tr>
        <tr>
            <td>N = 12800</td>
            <td>0.01315</td>
            <td> </td>
            <td>0.00140425</td>
        </tr>
    </tbody>
</table>



