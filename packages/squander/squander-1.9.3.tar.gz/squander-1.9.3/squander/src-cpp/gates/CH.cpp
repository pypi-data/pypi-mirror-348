/*
Created on Fri Jun 26 14:13:26 2020
Copyright 2020 Peter Rakyta, Ph.D.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: Peter Rakyta, Ph.D.
*/
/*! \file CH.cpp
    \brief Class representing a CH gate.
*/

#include "CH.h"



using namespace std;


/**
@brief Nullary constructor of the class.
*/
CH::CH() {

    // A string labeling the gate operation
    name = "CH";

    // number of qubits spanning the matrix of the gate
    qbit_num = -1;

    // the size of the matrix
    matrix_size = -1;

    // A string describing the type of the gate
    type = CH_OPERATION;

    // The number of free parameters
    parameter_num = 0;

    // The index of the qubit on which the gate acts (target_qbit >= 0)
    target_qbit = -1;

    // The index of the qubit which acts as a control qubit (control_qbit >= 0) in controlled gates
     control_qbit = -1;


}


/**
@brief Constructor of the class.
@param qbit_num_in The number of qubits in the unitaries
@param target_qbit_in The identification number of the target qubit. (0 <= target_qbit <= qbit_num-1)
@param control_qbit_in The identification number of the control qubit. (0 <= target_qbit <= qbit_num-1)
*/
CH::CH(int qbit_num_in,  int target_qbit_in, int control_qbit_in) {


    // A string labeling the gate operation
    name = "CH";

    // number of qubits spanning the matrix of the gate
    qbit_num = qbit_num_in;

    // the size of the matrix
    matrix_size = Power_of_2(qbit_num);

    // A string describing the type of the gate
    type = CH_OPERATION;

    // The number of free parameters
    parameter_num = 0;

    if (target_qbit_in >= qbit_num) {
       std::stringstream sstream;
       sstream << "The index of the target qubit is larger than the number of qubits" << std::endl;
       print(sstream, 0);	   
       throw sstream.str();
    }
  
    // The index of the qubit on which the gate acts (target_qbit >= 0)
    target_qbit = target_qbit_in;


    if (control_qbit_in >= qbit_num) {
       std::stringstream sstream;
       sstream << "The index of the control qubit is larger than the number of qubits" << std::endl;
       print(sstream, 0);	    		            
       throw sstream.str();
    }
   
    // The index of the qubit which acts as a control qubit (control_qbit >= 0) in controlled gates
    control_qbit = control_qbit_in;


}

/**
@brief Destructor of the class
*/
CH::~CH() {
}

/**
@brief Call to retrieve the gate matrix
@return Returns with the matrix of the gate
*/
Matrix
CH::get_matrix() {

    return get_matrix( false );
}


/**
@brief Call to retrieve the gate matrix
@param parallel Set 0 for sequential execution, 1 for parallel execution with OpenMP and 2 for parallel with TBB (optional)
@return Returns with the matrix of the gate
*/
Matrix
CH::get_matrix(int parallel) {

    Matrix CH_matrix = create_identity(matrix_size);
    apply_to(CH_matrix, parallel);

    return CH_matrix;
}



/**
@brief Call to apply the gate on the input array/matrix CH*input
@param input The input array on which the gate is applied
@param parallel Set 0 for sequential execution, 1 for parallel execution with OpenMP and 2 for parallel with TBB (optional)
*/
void 
CH::apply_to( Matrix& input, int parallel ) {

    if (input.rows != matrix_size ) {
        std::string err("CH::apply_to: Wrong input size in CH gate apply.");
        throw err;    
    }

    Matrix u3_1qbit = calc_one_qubit_u3();
    apply_kernel_to(u3_1qbit, input, false, parallel);

}



/**
@brief Call to apply the gate on the input array/matrix by input*CH
@param input The input array on which the gate is applied
*/
void 
CH::apply_from_right( Matrix& input ) {


    Matrix u3_1qbit = calc_one_qubit_u3();
    apply_kernel_from_right(u3_1qbit, input);

}


/**
@brief Call to set the number of qubits spanning the matrix of the gate
@param qbit_num The number of qubits
*/
void CH::set_qbit_num(int qbit_num) {
        // setting the number of qubits
        Gate::set_qbit_num(qbit_num);

}



/**
@brief Call to reorder the qubits in the matrix of the gate
@param qbit_list The reordered list of qubits spanning the matrix
*/
void CH::reorder_qubits( vector<int> qbit_list) {

        Gate::reorder_qubits(qbit_list);

}



/**
@brief Set static values for matrix of the gates.
@param u3_1qbit Matrix parameter for the gate.

*/
Matrix
CH::calc_one_qubit_u3( ){

    Matrix u3_1qbit = Matrix(2,2); 
    u3_1qbit[0].real = 1.0/sqrt(2); u3_1qbit[0].imag = 0.0; 
    u3_1qbit[1].real = 1.0/sqrt(2); u3_1qbit[1].imag = 0.0;
    u3_1qbit[2].real = 1.0/sqrt(2); u3_1qbit[2].imag = 0.0;
    u3_1qbit[3].real = -1.0/sqrt(2);u3_1qbit[3].imag = 0.0;
    return u3_1qbit;

}


/**
@brief Call to create a clone of the present class
@return Return with a pointer pointing to the cloned object
*/
CH* CH::clone() {

    CH* ret = new CH( qbit_num, target_qbit, control_qbit );
    
    ret->set_parameter_start_idx( get_parameter_start_idx() );
    ret->set_parents( parents );
    ret->set_children( children );

    return ret;

}



