/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace spirv {
class SamplingOpInterface;
namespace detail {
struct SamplingOpInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    ::mlir::TypedValue<::mlir::Type> (*getSampledImage)(const Concept *impl, ::mlir::Operation *);
    ::mlir::TypedValue<::mlir::Type> (*getCoordinate)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::spirv::SamplingOpInterface;
    Model() : Concept{getSampledImage, getCoordinate} {}

    static inline ::mlir::TypedValue<::mlir::Type> getSampledImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline ::mlir::TypedValue<::mlir::Type> getCoordinate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::spirv::SamplingOpInterface;
    FallbackModel() : Concept{getSampledImage, getCoordinate} {}

    static inline ::mlir::TypedValue<::mlir::Type> getSampledImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline ::mlir::TypedValue<::mlir::Type> getCoordinate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};
template <typename ConcreteOp>
struct SamplingOpInterfaceTrait;

} // namespace detail
class SamplingOpInterface : public ::mlir::OpInterface<SamplingOpInterface, detail::SamplingOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<SamplingOpInterface, detail::SamplingOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::SamplingOpInterfaceTrait<ConcreteOp> {};

  /// Get SampledImage of the operation.
  ::mlir::TypedValue<::mlir::Type> getSampledImage();

  /// Get Coordinate of the operation.
  ::mlir::TypedValue<::mlir::Type> getCoordinate();
};
namespace detail {
  template <typename ConcreteOp>
  struct SamplingOpInterfaceTrait : public ::mlir::OpInterface<SamplingOpInterface, detail::SamplingOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
} // namespace spirv
} // namespace mlir
namespace mlir {
namespace spirv {
class ExplicitLodOpInterface;
namespace detail {
struct ExplicitLodOpInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    /// The base classes of this interface.
    const ::mlir::spirv::SamplingOpInterface::Concept *implSamplingOpInterface = nullptr;

    void initializeInterfaceConcept(::mlir::detail::InterfaceMap &interfaceMap) {
      implSamplingOpInterface = interfaceMap.lookup<::mlir::spirv::SamplingOpInterface>();
      assert(implSamplingOpInterface && "`::mlir::spirv::ExplicitLodOpInterface` expected its base interface `::mlir::spirv::SamplingOpInterface` to be registered");
    }
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::spirv::ExplicitLodOpInterface;
    Model() : Concept{} {}

  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::spirv::ExplicitLodOpInterface;
    FallbackModel() : Concept{} {}

  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};
template <typename ConcreteOp>
struct ExplicitLodOpInterfaceTrait;

} // namespace detail
class ExplicitLodOpInterface : public ::mlir::OpInterface<ExplicitLodOpInterface, detail::ExplicitLodOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<ExplicitLodOpInterface, detail::ExplicitLodOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::ExplicitLodOpInterfaceTrait<ConcreteOp> {};
  //===----------------------------------------------------------------===//
  // Inherited from ::mlir::spirv::SamplingOpInterface
  //===----------------------------------------------------------------===//

  operator ::mlir::spirv::SamplingOpInterface () const {
    if (!*this) return nullptr;
    return ::mlir::spirv::SamplingOpInterface(*this, getImpl()->implSamplingOpInterface);
  }


  /// Get SampledImage of the operation.
  ::mlir::TypedValue<::mlir::Type> getSampledImage();

  /// Get Coordinate of the operation.
  ::mlir::TypedValue<::mlir::Type> getCoordinate();
};
namespace detail {
  template <typename ConcreteOp>
  struct ExplicitLodOpInterfaceTrait : public ::mlir::OpInterface<ExplicitLodOpInterface, detail::ExplicitLodOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
} // namespace spirv
} // namespace mlir
namespace mlir {
namespace spirv {
class ImplicitLodOpInterface;
namespace detail {
struct ImplicitLodOpInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    /// The base classes of this interface.
    const ::mlir::spirv::SamplingOpInterface::Concept *implSamplingOpInterface = nullptr;

    void initializeInterfaceConcept(::mlir::detail::InterfaceMap &interfaceMap) {
      implSamplingOpInterface = interfaceMap.lookup<::mlir::spirv::SamplingOpInterface>();
      assert(implSamplingOpInterface && "`::mlir::spirv::ImplicitLodOpInterface` expected its base interface `::mlir::spirv::SamplingOpInterface` to be registered");
    }
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::spirv::ImplicitLodOpInterface;
    Model() : Concept{} {}

  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::spirv::ImplicitLodOpInterface;
    FallbackModel() : Concept{} {}

  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};
template <typename ConcreteOp>
struct ImplicitLodOpInterfaceTrait;

} // namespace detail
class ImplicitLodOpInterface : public ::mlir::OpInterface<ImplicitLodOpInterface, detail::ImplicitLodOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<ImplicitLodOpInterface, detail::ImplicitLodOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::ImplicitLodOpInterfaceTrait<ConcreteOp> {};
  //===----------------------------------------------------------------===//
  // Inherited from ::mlir::spirv::SamplingOpInterface
  //===----------------------------------------------------------------===//

  operator ::mlir::spirv::SamplingOpInterface () const {
    if (!*this) return nullptr;
    return ::mlir::spirv::SamplingOpInterface(*this, getImpl()->implSamplingOpInterface);
  }


  /// Get SampledImage of the operation.
  ::mlir::TypedValue<::mlir::Type> getSampledImage();

  /// Get Coordinate of the operation.
  ::mlir::TypedValue<::mlir::Type> getCoordinate();
};
namespace detail {
  template <typename ConcreteOp>
  struct ImplicitLodOpInterfaceTrait : public ::mlir::OpInterface<ImplicitLodOpInterface, detail::ImplicitLodOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
} // namespace spirv
} // namespace mlir
namespace mlir {
namespace spirv {
class FetchOpInterface;
namespace detail {
struct FetchOpInterfaceInterfaceTraits {
  struct Concept {
    /// The methods defined by the interface.
    ::mlir::TypedValue<::mlir::Type> (*getImage)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::spirv::FetchOpInterface;
    Model() : Concept{getImage} {}

    static inline ::mlir::TypedValue<::mlir::Type> getImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::spirv::FetchOpInterface;
    FallbackModel() : Concept{getImage} {}

    static inline ::mlir::TypedValue<::mlir::Type> getImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};
template <typename ConcreteOp>
struct FetchOpInterfaceTrait;

} // namespace detail
class FetchOpInterface : public ::mlir::OpInterface<FetchOpInterface, detail::FetchOpInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<FetchOpInterface, detail::FetchOpInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::FetchOpInterfaceTrait<ConcreteOp> {};

  /// Get Image of the operation.
  ::mlir::TypedValue<::mlir::Type> getImage();
};
namespace detail {
  template <typename ConcreteOp>
  struct FetchOpInterfaceTrait : public ::mlir::OpInterface<FetchOpInterface, detail::FetchOpInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
} // namespace spirv
} // namespace mlir
namespace mlir {
namespace spirv {
template<typename ConcreteOp>
::mlir::TypedValue<::mlir::Type> detail::SamplingOpInterfaceInterfaceTraits::Model<ConcreteOp>::getSampledImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getSampledImage();
}
template<typename ConcreteOp>
::mlir::TypedValue<::mlir::Type> detail::SamplingOpInterfaceInterfaceTraits::Model<ConcreteOp>::getCoordinate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getCoordinate();
}
template<typename ConcreteOp>
::mlir::TypedValue<::mlir::Type> detail::SamplingOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getSampledImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getSampledImage(tablegen_opaque_val);
}
template<typename ConcreteOp>
::mlir::TypedValue<::mlir::Type> detail::SamplingOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getCoordinate(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getCoordinate(tablegen_opaque_val);
}
} // namespace spirv
} // namespace mlir
namespace mlir {
namespace spirv {
} // namespace spirv
} // namespace mlir
namespace mlir {
namespace spirv {
} // namespace spirv
} // namespace mlir
namespace mlir {
namespace spirv {
template<typename ConcreteOp>
::mlir::TypedValue<::mlir::Type> detail::FetchOpInterfaceInterfaceTraits::Model<ConcreteOp>::getImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getImage();
}
template<typename ConcreteOp>
::mlir::TypedValue<::mlir::Type> detail::FetchOpInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getImage(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getImage(tablegen_opaque_val);
}
} // namespace spirv
} // namespace mlir
