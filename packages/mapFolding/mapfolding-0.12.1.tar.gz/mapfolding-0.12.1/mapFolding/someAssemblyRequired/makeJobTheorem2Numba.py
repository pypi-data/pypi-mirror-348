from mapFolding import getPathFilenameFoldsTotal, MapFoldingState, packageSettings
from mapFolding.someAssemblyRequired import IfThis, raiseIfNoneGitHubIssueNumber3
from astToolkit import (
	Be,
	ClassIsAndAttribute,
	extractFunctionDef,
	IngredientsFunction,
	IngredientsModule,
	LedgerOfImports,
	Make,
	NodeChanger,
	NodeTourist,
	str_nameDOTname,
	Then,
)
from astToolkit.transformationTools import write_astModule
from mapFolding.someAssemblyRequired.RecipeJob import RecipeJobTheorem2Numba
from mapFolding.someAssemblyRequired.toolkitNumba import decorateCallableWithNumba, parametersNumbaLight, SpicesJobNumba
from mapFolding.syntheticModules.initializeCount import initializeGroupsOfFolds
from pathlib import PurePosixPath
from typing import cast, NamedTuple
from Z0Z_tools import autoDecodingRLE
import ast
"""Synthesize one file to compute `foldsTotal` of `mapShape`."""

listIdentifiersNotUsedAllHARDCODED = ['concurrencyLimit', 'foldsTotal', 'mapShape',]
listIdentifiersNotUsedParallelSequentialHARDCODED = ['indexLeaf']
listIdentifiersNotUsedSequentialHARDCODED = ['foldGroups', 'taskDivisions', 'taskIndex',]

listIdentifiersReplacedHARDCODED = ['groupsOfFolds',]

listIdentifiersStaticValuesHARDCODED = ['dimensionsTotal', 'leavesTotal',]

listIdentifiersNotUsedHARDCODED = listIdentifiersStaticValuesHARDCODED + listIdentifiersReplacedHARDCODED + listIdentifiersNotUsedAllHARDCODED + listIdentifiersNotUsedParallelSequentialHARDCODED + listIdentifiersNotUsedSequentialHARDCODED

def addLauncherNumbaProgress(ingredientsModule: IngredientsModule, ingredientsFunction: IngredientsFunction, job: RecipeJobTheorem2Numba, spices: SpicesJobNumba) -> tuple[IngredientsModule, IngredientsFunction]:
	"""
	Add progress tracking capabilities to a Numba-optimized function.

	This function modifies both the module and the function to integrate Numba-compatible
	progress tracking for long-running calculations. It performs several key transformations:

	1. Adds a progress bar parameter to the function signature
	2. Replaces counting increments with progress bar updates
	3. Creates a launcher section that displays and updates progress
	4. Configures file output to save results upon completion

	The progress tracking is particularly important for map folding calculations
	which can take hours or days to complete, providing visual feedback and
	estimated completion times.

	Parameters:
		ingredientsModule: The module where the function is defined.
		ingredientsFunction: The function to modify with progress tracking.
		job: Configuration specifying shape details and output paths.
		spices: Configuration specifying progress bar details.

	Returns:
		A tuple containing the modified module and function with progress tracking.
	"""
	linesLaunch: str = f"""
if __name__ == '__main__':
	with ProgressBar(total={job.foldsTotalEstimated}, update_interval=2) as statusUpdate:
		{job.countCallable}(statusUpdate)
		foldsTotal = statusUpdate.n * {job.state.leavesTotal}
		print('\\nmap {job.state.mapShape} =', foldsTotal)
		writeStream = open('{job.pathFilenameFoldsTotal.as_posix()}', 'w')
		writeStream.write(str(foldsTotal))
		writeStream.close()
"""
	numba_progressPythonClass: str = 'ProgressBar'
	numba_progressNumbaType: str = 'ProgressBarType'
	ingredientsModule.imports.addImportFrom_asStr('numba_progress', numba_progressPythonClass)
	ingredientsModule.imports.addImportFrom_asStr('numba_progress', numba_progressNumbaType)

	ast_argNumbaProgress = ast.arg(arg=spices.numbaProgressBarIdentifier, annotation=ast.Name(id=numba_progressPythonClass, ctx=ast.Load()))
	ingredientsFunction.astFunctionDef.args.args.append(ast_argNumbaProgress)

	findThis = ClassIsAndAttribute.targetIs(ast.AugAssign, IfThis.isNameIdentifier(job.shatteredDataclass.countingVariableName.id))
	doThat = Then.replaceWith(Make.Expr(Make.Call(Make.Attribute(Make.Name(spices.numbaProgressBarIdentifier),'update'),[Make.Constant(1)])))
	countWithProgressBar = NodeChanger(findThis, doThat)
	countWithProgressBar.visit(ingredientsFunction.astFunctionDef)

	removeReturnStatement = NodeChanger(Be.Return, Then.removeIt)
	removeReturnStatement.visit(ingredientsFunction.astFunctionDef)
	ingredientsFunction.astFunctionDef.returns = Make.Constant(value=None)

	ingredientsModule.appendLauncher(ast.parse(linesLaunch))

	return ingredientsModule, ingredientsFunction

def move_arg2FunctionDefDOTbodyAndAssignInitialValues(ingredientsFunction: IngredientsFunction, job: RecipeJobTheorem2Numba) -> IngredientsFunction:
	"""
	Convert function parameters into initialized variables with concrete values.

	This function implements a critical transformation that converts function parameters
	into statically initialized variables in the function body. This enables several
	optimizations:

	1. Eliminating parameter passing overhead.
	2. Embedding concrete values directly in the code.
	3. Allowing Numba to optimize based on known value characteristics.
	4. Simplifying function signatures for specialized use cases.

	The function handles different data types (scalars, arrays, custom types) appropriately,
	replacing abstract parameter references with concrete values from the computation state.
	It also removes unused parameters and variables to eliminate dead code.

	Parameters:
		ingredientsFunction: The function to transform.
		job: Recipe containing concrete values for parameters and field metadata.

	Returns:
		The modified function with parameters converted to initialized variables.
	"""
	ingredientsFunction.imports.update(job.shatteredDataclass.imports)

	list_argCuzMyBrainRefusesToThink = ingredientsFunction.astFunctionDef.args.args + ingredientsFunction.astFunctionDef.args.posonlyargs + ingredientsFunction.astFunctionDef.args.kwonlyargs
	list_arg_arg: list[str] = [ast_arg.arg for ast_arg in list_argCuzMyBrainRefusesToThink]
	listName: list[ast.Name] = []
	NodeTourist(Be.Name, Then.appendTo(listName)).visit(ingredientsFunction.astFunctionDef)
	listIdentifiers: list[str] = [astName.id for astName in listName]
	listIdentifiersNotUsed: list[str] = list(set(list_arg_arg) - set(listIdentifiers))

	for ast_arg in list_argCuzMyBrainRefusesToThink:
		if ast_arg.arg in job.shatteredDataclass.field2AnnAssign:
			if ast_arg.arg in listIdentifiersNotUsed:
				pass
			else:
				ImaAnnAssign, elementConstructor = job.shatteredDataclass.Z0Z_field2AnnAssign[ast_arg.arg]
				match elementConstructor:
					case 'scalar':
						cast(ast.Constant, cast(ast.Call, ImaAnnAssign.value).args[0]).value = int(job.state.__dict__[ast_arg.arg])
					case 'array':
						dataAsStrRLE: str = autoDecodingRLE(job.state.__dict__[ast_arg.arg], True)
						dataAs_astExpr: ast.expr = cast(ast.Expr, ast.parse(dataAsStrRLE).body[0]).value
						cast(ast.Call, ImaAnnAssign.value).args = [dataAs_astExpr]
					case _:
						list_exprDOTannotation: list[ast.expr] = []
						list_exprDOTvalue: list[ast.expr] = []
						for dimension in job.state.mapShape:
							list_exprDOTannotation.append(Make.Name(elementConstructor))
							list_exprDOTvalue.append(Make.Call(Make.Name(elementConstructor), [Make.Constant(dimension)]))
						cast(ast.Tuple, cast(ast.Subscript, cast(ast.AnnAssign, ImaAnnAssign).annotation).slice).elts = list_exprDOTannotation
						cast(ast.Tuple, ImaAnnAssign.value).elts = list_exprDOTvalue

				ingredientsFunction.astFunctionDef.body.insert(0, ImaAnnAssign)

			findThis = IfThis.is_argIdentifier(ast_arg.arg)
			remove_arg = NodeChanger(findThis, Then.removeIt)
			remove_arg.visit(ingredientsFunction.astFunctionDef)

	ast.fix_missing_locations(ingredientsFunction.astFunctionDef)
	return ingredientsFunction

def makeJobNumba(job: RecipeJobTheorem2Numba, spices: SpicesJobNumba) -> None:

	astFunctionDef = extractFunctionDef(job.source_astModule, job.countCallable)
	if not astFunctionDef: raise raiseIfNoneGitHubIssueNumber3
	ingredientsCount: IngredientsFunction = IngredientsFunction(astFunctionDef, LedgerOfImports())

	# Remove `foldGroups` and any other unused statements, so you can dynamically determine which variables are not used
	findThis = ClassIsAndAttribute.targetsIs(ast.Assign, lambda list_expr: any([IfThis.isSubscriptIdentifier('foldGroups')(node) for node in list_expr ]))
	# findThis = IfThis.isAssignAndTargets0Is(IfThis.isSubscriptIdentifier('foldGroups'))
	doThat = Then.removeIt
	remove_foldGroups = NodeChanger(findThis, doThat)
	# remove_foldGroups.visit(ingredientsCount.astFunctionDef)

	# replace identifiers with static values with their values, so you can dynamically determine which variables are not used
	listIdentifiersStaticValues = listIdentifiersStaticValuesHARDCODED
	for identifier in listIdentifiersStaticValues:
		findThis = IfThis.isNameIdentifier(identifier)
		doThat = Then.replaceWith(Make.Constant(int(job.state.__dict__[identifier])))
		NodeChanger(findThis, doThat).visit(ingredientsCount.astFunctionDef)

	ingredientsModule = IngredientsModule()
	# This launcher eliminates the use of one identifier, so run it now and you can dynamically determine which variables are not used
	if spices.useNumbaProgressBar:
		ingredientsModule, ingredientsCount = addLauncherNumbaProgress(ingredientsModule, ingredientsCount, job, spices)
		spices.parametersNumba['nogil'] = True
	else:
		linesLaunch: str = f"""
if __name__ == '__main__':
	import time
	timeStart = time.perf_counter()
	foldsTotal = int({job.countCallable}() * {job.state.leavesTotal})
	print(time.perf_counter() - timeStart)
	print('\\nmap {job.state.mapShape} =', foldsTotal)
	writeStream = open('{job.pathFilenameFoldsTotal.as_posix()}', 'w')
	writeStream.write(str(foldsTotal))
	writeStream.close()
"""
	# from mapFolding.oeis import getFoldsTotalKnown
	# print(foldsTotal == getFoldsTotalKnown({job.state.mapShape}))
		ingredientsModule.appendLauncher(ast.parse(linesLaunch))
		changeReturnParallelCallable = NodeChanger(Be.Return, Then.replaceWith(Make.Return(job.shatteredDataclass.countingVariableName)))
		changeReturnParallelCallable.visit(ingredientsCount.astFunctionDef)
		ingredientsCount.astFunctionDef.returns = job.shatteredDataclass.countingVariableAnnotation

	ingredientsCount = move_arg2FunctionDefDOTbodyAndAssignInitialValues(ingredientsCount, job)

	class DatatypeConfig(NamedTuple):
		Z0Z_module: str_nameDOTname
		fml: str
		Z0Z_type_name: str
		Z0Z_asname: str | None = None

	listDatatypeConfigs = [
		DatatypeConfig(fml='DatatypeLeavesTotal', Z0Z_module='numba', Z0Z_type_name='uint8'),
		DatatypeConfig(fml='DatatypeElephino', Z0Z_module='numba', Z0Z_type_name='uint16'),
		DatatypeConfig(fml='DatatypeFoldsTotal', Z0Z_module='numba', Z0Z_type_name='uint64'),
	]

	for datatypeConfig in listDatatypeConfigs:
		ingredientsModule.imports.addImportFrom_asStr(datatypeConfig.Z0Z_module, datatypeConfig.Z0Z_type_name)
		statement = Make.Assign(
			[Make.Name(datatypeConfig.fml, ast.Store())],
			Make.Name(datatypeConfig.Z0Z_type_name)
		)
		ingredientsModule.appendPrologue(statement=statement)

	ingredientsCount.imports.removeImportFromModule('mapFolding.theSSOT')

	listNumPyTypeConfigs = [
		DatatypeConfig(fml='Array1DLeavesTotal', Z0Z_module='numpy', Z0Z_type_name='uint8', Z0Z_asname='Array1DLeavesTotal'),
		DatatypeConfig(fml='Array1DElephino', Z0Z_module='numpy', Z0Z_type_name='uint16', Z0Z_asname='Array1DElephino'),
		DatatypeConfig(fml='Array3D', Z0Z_module='numpy', Z0Z_type_name='uint8', Z0Z_asname='Array3D'),
	]

	for typeConfig in listNumPyTypeConfigs:
		ingredientsCount.imports.removeImportFrom(typeConfig.Z0Z_module, None, typeConfig.fml)
		ingredientsCount.imports.addImportFrom_asStr(typeConfig.Z0Z_module, typeConfig.Z0Z_type_name, typeConfig.Z0Z_asname)

	ingredientsCount.astFunctionDef.decorator_list = [] # TODO low-priority, handle this more elegantly
	# TODO when I add the function signature in numba style back to the decorator, the logic needs to handle `ProgressBarType:`
	ingredientsCount = decorateCallableWithNumba(ingredientsCount, spices.parametersNumba)

	ingredientsModule.appendIngredientsFunction(ingredientsCount)
	write_astModule(ingredientsModule, job.pathFilenameModule, job.packageIdentifier)

	"""
	Overview
	- the code starts life in theDao.py, which has many optimizations;
		- `makeNumbaOptimizedFlow` increase optimization especially by using numba;
		- `makeJobNumba` increases optimization especially by limiting its capabilities to just one set of parameters
	- the synthesized module must run well as a standalone interpreted-Python script
	- the next major optimization step will (probably) be to use the module synthesized by `makeJobNumba` to compile a standalone executable
	- Nevertheless, at each major optimization step, the code is constantly being improved and optimized, so everything must be well organized (read: semantic) and able to handle a range of arbitrary upstream and not disrupt downstream transformations

	Necessary
	- Move the function's parameters to the function body,
	- initialize identifiers with their state types and values,

	Optimizations
	- replace static-valued identifiers with their values
	- narrowly focused imports

	Minutia
	- do not use `with` statement inside numba jitted code, except to use numba's obj mode
	"""

if __name__ == '__main__':
	mapShape = (2,4)
	state = MapFoldingState(mapShape)
	state = initializeGroupsOfFolds(state)
	# foldsTotalEstimated = getFoldsTotalKnown(state.mapShape) // state.leavesTotal
	# foldsTotalEstimated = dictionaryEstimates[state.mapShape] // state.leavesTotal
	foldsTotalEstimated = 0
	pathModule = PurePosixPath(packageSettings.pathPackage, 'jobs')
	pathFilenameFoldsTotal = PurePosixPath(getPathFilenameFoldsTotal(state.mapShape, pathModule))
	aJob = RecipeJobTheorem2Numba(state, foldsTotalEstimated, pathModule=pathModule, pathFilenameFoldsTotal=pathFilenameFoldsTotal)
	spices = SpicesJobNumba(useNumbaProgressBar=False, parametersNumba=parametersNumbaLight)
	# spices = SpicesJobNumba()
	makeJobNumba(aJob, spices)
