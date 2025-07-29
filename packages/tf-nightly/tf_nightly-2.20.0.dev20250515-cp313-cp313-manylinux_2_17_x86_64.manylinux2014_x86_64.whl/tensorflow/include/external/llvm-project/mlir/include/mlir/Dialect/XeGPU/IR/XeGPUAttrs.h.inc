/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir {
namespace xegpu {
class BlockTensorDescAttr;
class ScatterTensorDescAttr;
class MemorySpaceAttr;
class CachePolicyAttr;
class FenceScopeAttr;
class LayoutAttr;
namespace detail {
struct BlockTensorDescAttrStorage;
} // namespace detail
class BlockTensorDescAttr : public ::mlir::Attribute::AttrBase<BlockTensorDescAttr, ::mlir::Attribute, detail::BlockTensorDescAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "xegpu.block_tdesc_attr";
  static constexpr ::llvm::StringLiteral dialectName = "xegpu";
  static BlockTensorDescAttr get(::mlir::MLIRContext *context, MemorySpaceAttr memory_space, IntegerAttr array_length, BoolAttr boundary_check);
  static BlockTensorDescAttr get(::mlir::MLIRContext *context, xegpu::MemorySpace memory_space = xegpu::MemorySpace::Global, int array_length = 1, bool boundary_check = true);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"block_tdesc_attr"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  MemorySpaceAttr getMemorySpace() const;
  IntegerAttr getArrayLength() const;
  BoolAttr getBoundaryCheck() const;
};
namespace detail {
struct ScatterTensorDescAttrStorage;
} // namespace detail
class ScatterTensorDescAttr : public ::mlir::Attribute::AttrBase<ScatterTensorDescAttr, ::mlir::Attribute, detail::ScatterTensorDescAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "xegpu.scatter_tdesc_attr";
  static constexpr ::llvm::StringLiteral dialectName = "xegpu";
  using Base::getChecked;
  static ScatterTensorDescAttr get(::mlir::MLIRContext *context, MemorySpaceAttr memory_space, IntegerAttr chunk_size);
  static ScatterTensorDescAttr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, MemorySpaceAttr memory_space, IntegerAttr chunk_size);
  static ScatterTensorDescAttr get(::mlir::MLIRContext *context, xegpu::MemorySpace memory_space = xegpu::MemorySpace::Global, int chunk_size = 1);
  static ScatterTensorDescAttr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, xegpu::MemorySpace memory_space = xegpu::MemorySpace::Global, int chunk_size = 1);
  static ::llvm::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, MemorySpaceAttr memory_space, IntegerAttr chunk_size);
  static ::llvm::LogicalResult verifyInvariants(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, MemorySpaceAttr memory_space, IntegerAttr chunk_size);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"scatter_tdesc_attr"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  MemorySpaceAttr getMemorySpace() const;
  IntegerAttr getChunkSize() const;
};
namespace detail {
struct MemorySpaceAttrStorage;
} // namespace detail
class MemorySpaceAttr : public ::mlir::Attribute::AttrBase<MemorySpaceAttr, ::mlir::Attribute, detail::MemorySpaceAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "xegpu.memory_space";
  static constexpr ::llvm::StringLiteral dialectName = "xegpu";
  static MemorySpaceAttr get(::mlir::MLIRContext *context, ::mlir::xegpu::MemorySpace value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"memory_space"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::xegpu::MemorySpace getValue() const;
};
namespace detail {
struct CachePolicyAttrStorage;
} // namespace detail
class CachePolicyAttr : public ::mlir::Attribute::AttrBase<CachePolicyAttr, ::mlir::Attribute, detail::CachePolicyAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "xegpu.cache_hint";
  static constexpr ::llvm::StringLiteral dialectName = "xegpu";
  static CachePolicyAttr get(::mlir::MLIRContext *context, ::mlir::xegpu::CachePolicy value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"cache_hint"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::xegpu::CachePolicy getValue() const;
};
namespace detail {
struct FenceScopeAttrStorage;
} // namespace detail
class FenceScopeAttr : public ::mlir::Attribute::AttrBase<FenceScopeAttr, ::mlir::Attribute, detail::FenceScopeAttrStorage> {
public:
  using Base::Base;
  static constexpr ::llvm::StringLiteral name = "xegpu.fence_scope";
  static constexpr ::llvm::StringLiteral dialectName = "xegpu";
  static FenceScopeAttr get(::mlir::MLIRContext *context, ::mlir::xegpu::FenceScope value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"fence_scope"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::xegpu::FenceScope getValue() const;
};
namespace detail {
struct LayoutAttrStorage;
} // namespace detail
class LayoutAttr : public ::mlir::Attribute::AttrBase<LayoutAttr, ::mlir::Attribute, detail::LayoutAttrStorage> {
public:
  using Base::Base;
  bool isWgLayout() {
    return getSgLayout() != nullptr;
  }

  bool isSgLayout() {
    return getSgLayout() == nullptr && getLaneLayout() != nullptr;
  }

  int64_t getRank() {
    if (auto attr = getSgLayout())
      return attr.size();
    if (auto attr = getInstData())
      return attr.size();
    if (auto attr = getLaneLayout())
      return attr.size();
    return 0;
  }
  static constexpr ::llvm::StringLiteral name = "xegpu.layout";
  static constexpr ::llvm::StringLiteral dialectName = "xegpu";
  using Base::getChecked;
  static LayoutAttr get(::mlir::MLIRContext *context, DenseI32ArrayAttr sg_layout, DenseI32ArrayAttr sg_data, DenseI32ArrayAttr inst_data, DenseI32ArrayAttr lane_layout, DenseI32ArrayAttr lane_data, DenseI32ArrayAttr order);
  static LayoutAttr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, DenseI32ArrayAttr sg_layout, DenseI32ArrayAttr sg_data, DenseI32ArrayAttr inst_data, DenseI32ArrayAttr lane_layout, DenseI32ArrayAttr lane_data, DenseI32ArrayAttr order);
  static LayoutAttr get(::mlir::MLIRContext *context, llvm::ArrayRef<int> lane_layout, llvm::ArrayRef<int> lane_data);
  static LayoutAttr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, llvm::ArrayRef<int> lane_layout, llvm::ArrayRef<int> lane_data);
  static ::llvm::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, DenseI32ArrayAttr sg_layout, DenseI32ArrayAttr sg_data, DenseI32ArrayAttr inst_data, DenseI32ArrayAttr lane_layout, DenseI32ArrayAttr lane_data, DenseI32ArrayAttr order);
  static ::llvm::LogicalResult verifyInvariants(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, DenseI32ArrayAttr sg_layout, DenseI32ArrayAttr sg_data, DenseI32ArrayAttr inst_data, DenseI32ArrayAttr lane_layout, DenseI32ArrayAttr lane_data, DenseI32ArrayAttr order);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"layout"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  DenseI32ArrayAttr getSgLayout() const;
  DenseI32ArrayAttr getSgData() const;
  DenseI32ArrayAttr getInstData() const;
  DenseI32ArrayAttr getLaneLayout() const;
  DenseI32ArrayAttr getLaneData() const;
  DenseI32ArrayAttr getOrder() const;
};
} // namespace xegpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xegpu::BlockTensorDescAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xegpu::ScatterTensorDescAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xegpu::MemorySpaceAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xegpu::CachePolicyAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xegpu::FenceScopeAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::xegpu::LayoutAttr)

#endif  // GET_ATTRDEF_CLASSES

