/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace bufferization {
class TensorLikeType;
namespace detail {
struct TensorLikeTypeInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
  };
  template<typename ConcreteType>
  class Model : public Concept {
  public:
    using Interface = ::mlir::bufferization::TensorLikeType;
    Model() : Concept{} {}

  };
  template<typename ConcreteType>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::bufferization::TensorLikeType;
    FallbackModel() : Concept{} {}

  };
  template<typename ConcreteModel, typename ConcreteType>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteType;
  };
};
template <typename ConcreteType>
struct TensorLikeTypeTrait;

} // namespace detail
class TensorLikeType : public ::mlir::TypeInterface<TensorLikeType, detail::TensorLikeTypeInterfaceTraits> {
public:
  using ::mlir::TypeInterface<TensorLikeType, detail::TensorLikeTypeInterfaceTraits>::TypeInterface;
  template <typename ConcreteType>
  struct Trait : public detail::TensorLikeTypeTrait<ConcreteType> {};
};
namespace detail {
  template <typename ConcreteType>
  struct TensorLikeTypeTrait : public ::mlir::TypeInterface<TensorLikeType, detail::TensorLikeTypeInterfaceTraits>::Trait<ConcreteType> {
  };
}// namespace detail
} // namespace bufferization
} // namespace mlir
namespace mlir {
namespace bufferization {
class BufferLikeType;
namespace detail {
struct BufferLikeTypeInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
  };
  template<typename ConcreteType>
  class Model : public Concept {
  public:
    using Interface = ::mlir::bufferization::BufferLikeType;
    Model() : Concept{} {}

  };
  template<typename ConcreteType>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::bufferization::BufferLikeType;
    FallbackModel() : Concept{} {}

  };
  template<typename ConcreteModel, typename ConcreteType>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteType;
  };
};
template <typename ConcreteType>
struct BufferLikeTypeTrait;

} // namespace detail
class BufferLikeType : public ::mlir::TypeInterface<BufferLikeType, detail::BufferLikeTypeInterfaceTraits> {
public:
  using ::mlir::TypeInterface<BufferLikeType, detail::BufferLikeTypeInterfaceTraits>::TypeInterface;
  template <typename ConcreteType>
  struct Trait : public detail::BufferLikeTypeTrait<ConcreteType> {};
};
namespace detail {
  template <typename ConcreteType>
  struct BufferLikeTypeTrait : public ::mlir::TypeInterface<BufferLikeType, detail::BufferLikeTypeInterfaceTraits>::Trait<ConcreteType> {
  };
}// namespace detail
} // namespace bufferization
} // namespace mlir
namespace mlir {
namespace bufferization {
} // namespace bufferization
} // namespace mlir
namespace mlir {
namespace bufferization {
} // namespace bufferization
} // namespace mlir
