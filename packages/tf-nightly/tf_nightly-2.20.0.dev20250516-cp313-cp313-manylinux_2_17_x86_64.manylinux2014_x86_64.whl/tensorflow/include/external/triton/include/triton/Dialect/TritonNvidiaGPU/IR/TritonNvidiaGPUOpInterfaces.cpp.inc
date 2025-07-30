/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/


/// Return the A operand.
::mlir::TypedValue<::mlir::triton::gpu::MemDescType> mlir::triton::nvidia_gpu::MMAv5OpInterface::getA() {
      return getImpl()->getA(getImpl(), getOperation());
  }

/// Return the accumulator init flag.
::mlir::Value mlir::triton::nvidia_gpu::MMAv5OpInterface::useAccumulator() {
      return getImpl()->useAccumulator(getImpl(), getOperation());
  }

/// Set the accumulator init flag.
void mlir::triton::nvidia_gpu::MMAv5OpInterface::setUseAccumulator(::mlir::Value flag) {
      return getImpl()->setUseAccumulator(getImpl(), getOperation(), flag);
  }

/// Associate a new completion barrier to this MMAv5 op.
void mlir::triton::nvidia_gpu::MMAv5OpInterface::addCompletionBarrier(::mlir::Value barrier, ::mlir::Value pred) {
      return getImpl()->addCompletionBarrier(getImpl(), getOperation(), barrier, pred);
  }

/// Return the accumulator.
::mlir::TypedValue<::mlir::triton::gpu::MemDescType> mlir::triton::nvidia_gpu::MMAv5OpInterface::getAccumulator() {
      return getImpl()->getAccumulator(getImpl(), getOperation());
  }

/// Set the accumulator.
void mlir::triton::nvidia_gpu::MMAv5OpInterface::setAccumulator(::mlir::Value accum) {
      return getImpl()->setAccumulator(getImpl(), getOperation(), accum);
  }

/// Return the predicate of this op.
::mlir::Value mlir::triton::nvidia_gpu::MMAv5OpInterface::getPredicate() {
      return getImpl()->getPredicate(getImpl(), getOperation());
  }

/// Set the predicate of this op.
void mlir::triton::nvidia_gpu::MMAv5OpInterface::setPredicate(::mlir::Value pred) {
      return getImpl()->setPredicate(getImpl(), getOperation(), pred);
  }
