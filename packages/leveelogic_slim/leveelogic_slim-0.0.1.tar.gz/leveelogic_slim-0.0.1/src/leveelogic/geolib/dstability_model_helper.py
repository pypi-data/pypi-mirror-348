from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    PersistableSoil,
    AnalysisTypeEnum,
    WaternetCreatorSettings,
    PersistableElevation,
    PersistablePoint,
)
from geolib.models.dstability.analysis import (
    DStabilityBishopBruteForceAnalysisMethod,
    DStabilitySearchGrid,
    DStabilitySlipPlaneConstraints,
)
from geolib.models.dstability.loads import UniformLoad, Consolidation
from geolib.geometry.one import Point
from typing import Optional, List, Tuple, Dict
from pathlib import Path

from shapely import Polygon, MultiPolygon, get_coordinates
from shapely.ops import orient, unary_union

from ..helpers import polyline_polyline_intersections, is_point_in_or_on_polygon
from ..settings import DEFAULT_LOAD_CONSOLIDATION, DEFAULT_LOAD_SPREAD


class SoilPolygon:
    def __init__(self, points: List[Tuple[float, float]], soilcode: str):
        self.points = points
        self.soilcode = soilcode

    def to_shapely(self) -> Polygon:
        return Polygon(self.points)

    def __repr__(self) -> str:
        return f"SoilPolygon(soilcode={self.soilcode}, points={self.points})"


class DStabilityModelHelper:
    def __init__(self, model: DStabilityModel):
        self.model = model

    @classmethod
    def from_stix(cls, stix_file: str) -> "DStabilityModelHelper":
        ds = DStabilityModel()
        ds.parse(Path(stix_file))
        return DStabilityModelHelper(ds)

    def analysis_type(
        self, scenario_index: int = 0, calculation_index: int = 0
    ) -> Optional[AnalysisTypeEnum]:
        cs = self.model._get_calculation_settings(scenario_index, calculation_index)

        if cs is not None:
            return cs.AnalysisType

        return None

    def layer_intersections_at(
        self, x: float, scenario_index: int = 0, stage_index: int = 0
    ) -> List[Tuple[float, float, PersistableSoil]]:
        """Get the intersection with the layers at the given x

        Args:
            x (float): The x coordinate
            scenario_index (int, optional): index of the scenario. Defaults to 0.
            stage_index (int, optional): index of the stage in the scenario. Defaults to 0.

        Returns:
            List[Tuple[float, float, PersistableSoil]]: A list with top, bottom and soil tuples
        """
        geometry = self.model._get_geometry(scenario_index, stage_index)

        try:
            result = []
            line_points = [
                (x, self.top(scenario_index, stage_index) + 0.01),
                (x, self.bottom(scenario_index, stage_index) - 0.01),
            ]
            for layer in geometry.Layers:
                layer_points = [(p.X, p.Z) for p in layer.Points]
                for intersection in polyline_polyline_intersections(
                    line_points, layer_points
                ):
                    result.append(round(intersection[1], 3))

            result = sorted(
                list(set(result)), reverse=True
            )  # sort top to bottom and remove duplicates

            # now remove the intersection with no height
            final_result = []
            for i in range(1, len(result)):
                top = result[i - 1]
                bottom = result[i]
                layer = self.soillayer_at(
                    x=x,
                    z=(top + bottom) / 2.0,
                    scenario_index=scenario_index,
                    stage_index=stage_index,
                )

                if layer is None:
                    raise ValueError(
                        f"No layer found at x={x} and z={(top + bottom) / 2.0}"
                    )

                final_result.append(
                    {"top": top, "bottom": bottom, "soil": layer["soil"]}
                )

        except Exception as e:
            raise e

        return final_result

    def z_at(
        self,
        x: float,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> Optional[float]:
        intersections = self.layer_intersections_at(x, scenario_index, stage_index)
        if len(intersections) > 0:
            return intersections[0]["top"]
        else:
            return None

    def phreatic_level_at(
        self,
        x: float,
        scenario_index: int = 0,
        stage_index: int = 0,
        return_last_point_if_no_result: bool = False,
    ):
        plline = self.phreatic_line(scenario_index, stage_index)
        if len(plline) == 0:
            raise ValueError("No phreatic line found")

        intersections = polyline_polyline_intersections(
            [
                (x, self.top(scenario_index, stage_index) + 0.01),
                (x, self.bottom(scenario_index, stage_index) - 0.01),
            ],
            plline,
        )

        if len(intersections) == 0:
            if return_last_point_if_no_result:
                return plline[-1][1]
            else:
                return None

        return intersections[0][1]

    def phreatic_line(
        self,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> Optional[List[Tuple[float, float]]]:
        """Get the phreatic line of the model

        Args:
            model (DStabilityModel): the model
            scenario_index (int, optional): scenario. Defaults to 0.
            stage_index (int, optional): stage. Defaults to 0.

        Returns:
            List[Tuple[float, float]]: The phreatic line or None if not available
        """
        wnet = self.model._get_waternet(scenario_index, stage_index)
        phreatic_headline_id = wnet.PhreaticLineId

        if phreatic_headline_id is None:
            return None

        for headline in wnet.HeadLines:
            if headline.Id == phreatic_headline_id:
                return [(p.X, p.Z) for p in headline.Points]

    def set_phreatic_line(
        self,
        points: List[Tuple[float, float]],
        scenario_index: int = 0,
        stage_index: int = 0,
    ):
        wnet = self.model._get_waternet(scenario_index, stage_index)
        phreatic_headline_id = wnet.PhreaticLineId

        if phreatic_headline_id is None:
            self.model.add_head_line(
                points=[Point(x=p[0], z=p[1]) for p in points],
                label="Phreatic Line",
                is_phreatic_line=True,
            )
        else:
            for headline in wnet.HeadLines:
                if headline.Id == phreatic_headline_id:
                    headline.Points = [PersistablePoint(X=p[0], Z=p[1]) for p in points]
                    break

    def surface(
        self,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> List[Tuple[float, float]]:
        geometry = self.model._get_geometry(scenario_index, stage_index)
        points, polygons = [], []
        for layer in geometry.Layers:
            points += [(float(p.X), float(p.Z)) for p in layer.Points]
            polygons.append(Polygon([(float(p.X), float(p.Z)) for p in layer.Points]))

        boundary = orient(unary_union(polygons), sign=-1)
        boundary = [
            (round(p[0], 3), round(p[1], 3))
            for p in list(zip(*boundary.exterior.coords.xy))[:-1]
        ]
        # get the leftmost point
        left = min([p[0] for p in boundary])
        topleft_point = sorted(
            [p for p in boundary if p[0] == left], key=lambda x: x[1]
        )[-1]

        # get the rightmost points
        right = max([p[0] for p in boundary])
        rightmost_point = sorted(
            [p for p in boundary if p[0] == right], key=lambda x: x[1]
        )[-1]

        # get the index of leftmost point
        idx_left = boundary.index(topleft_point)
        surface = boundary[idx_left:] + boundary[:idx_left]

        # get the index of the rightmost point
        idx_right = surface.index(rightmost_point)
        surface = surface[: idx_right + 1]
        return surface

    def points(
        self,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> List[Tuple[float, float]]:

        geometry = self.model._get_geometry(scenario_index, stage_index)
        points = []
        for layer in geometry.Layers:
            points += [(p.X, p.Z) for p in layer.Points]
        return points

    def top(
        self,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> Optional[float]:
        points = self.points(scenario_index, stage_index)
        return max([p[1] for p in points])

    def bottom(
        self,
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> Optional[float]:
        points = self.points(scenario_index, stage_index)
        return min([p[1] for p in points])

    def left(self, scenario_index: int = 0, stage_index: int = 0) -> Optional[float]:
        points = self.points(scenario_index, stage_index)
        return min([p[0] for p in points])

    def right(self, scenario_index: int = 0, stage_index: int = 0) -> Optional[float]:
        points = self.points(scenario_index, stage_index)
        return max([p[0] for p in points])

    def sga_to_bff(
        self,
        scenario_index: int = 0,
        calculation_index: int = 0,
        add_constraints: bool = True,
    ):
        analysis_type = self.analysis_type(scenario_index, calculation_index)
        if analysis_type != AnalysisTypeEnum.SPENCER_GENETIC:
            raise ValueError(
                f"Trying to convert a '{analysis_type}' to a Spencer Genetic Algorithm, this only works for Bishop Brute Force calculation"
            )

        cs = self.model._get_calculation_settings(
            scenario_index=scenario_index, calculation_index=calculation_index
        )
        spencer_settings = cs.SpencerGenetic

        slip_plane_a = [(p.X, p.Z) for p in spencer_settings.SlipPlaneA]
        slip_plane_b = [(p.X, p.Z) for p in spencer_settings.SlipPlaneB]

        # either SlipPlaneA or SlipPlaneB can be the upper one so check
        # which one is the actaul lowest line by looking for the lowest
        # z coord (lines cannot cross so the lowest point is part of the lowest line)
        z_min_a = min([p[1] for p in slip_plane_a])
        z_min_b = min([p[1] for p in slip_plane_b])

        if z_min_a < z_min_b:
            upper_line = slip_plane_b
            lower_line = slip_plane_a
        else:
            upper_line = slip_plane_a
            lower_line = slip_plane_b

        ul_top = max([p[1] for p in upper_line])
        ul_bot = min([p[1] for p in upper_line])
        ul_left = upper_line[0][0]
        ul_right = upper_line[-1][0]
        ll_bot = min([p[1] for p in lower_line])
        ll_left = lower_line[0][0]
        ll_right = lower_line[-1][0]

        self.set_bbf(
            left=ul_left,
            bottom=ul_top + (ul_top - ul_bot),
            space=(ul_right - ul_left) / 10,
            numx=10,
            numz=10,
            bottom_tangent=ll_bot,
            space_tangent=(ul_bot - ll_bot) / 10,
            numt=10,
            scenario_index=scenario_index,
            calculation_index=calculation_index,
            add_constraints=add_constraints,
            in_left=ll_left,
            in_right=ul_left,
            out_left=ul_right,
            out_right=ll_right,
        )

    def set_bbf(
        self,
        left: float,
        bottom: float,
        space: float,
        numx: int,
        numz: int,
        bottom_tangent: float,
        space_tangent: float,
        numt: int,
        scenario_index: int = 0,
        calculation_index: int = 0,
        add_constraints: bool = True,
        in_left: float = None,
        in_right: float = None,
        out_left: float = None,
        out_right: float = None,
        min_slipplane_length: float = 0.0,
        min_slipplane_depth: float = 0.0,
    ):

        if add_constraints:
            is_size_constraints_enabled = (
                min_slipplane_length > 0.0 or min_slipplane_depth > 0.0
            )
            is_zone_a_constraints_enabled = in_left is not None and in_right is not None
            is_zone_b_constraints_enabled = (
                out_left is not None and out_right is not None
            )

            if is_zone_a_constraints_enabled:
                width_zone_a = in_right - in_left
                x_left_zone_a = in_left
            else:
                width_zone_a = 0.0
                x_left_zone_a = 0.0

            if is_zone_b_constraints_enabled:
                width_zone_b = out_right - out_left
                x_left_zone_b = out_left
            else:
                width_zone_b = 0.0
                x_left_zone_b = 0.0

            constraints = DStabilitySlipPlaneConstraints(
                is_size_constraints_enabled=is_size_constraints_enabled,
                is_zone_a_constraints_enabled=is_zone_a_constraints_enabled,
                is_zone_b_constraints_enabled=is_zone_b_constraints_enabled,
                minimum_slip_plane_depth=min_slipplane_depth,
                minimum_slip_plane_length=min_slipplane_length,
                x_left_zone_a=x_left_zone_a,
                x_left_zone_b=x_left_zone_b,
                width_zone_a=width_zone_a,
                width_zone_b=width_zone_b,
            )
        else:
            constraints = DStabilitySlipPlaneConstraints()

        self.model.set_model(
            DStabilityBishopBruteForceAnalysisMethod(
                search_grid=DStabilitySearchGrid(
                    bottom_left=Point(x=left, z=bottom),
                    number_of_points_in_x=numx,
                    number_of_points_in_z=numz,
                    space=space,
                ),
                bottom_tangent_line_z=bottom_tangent,
                number_of_tangent_lines=numt,
                space_tangent_lines=space_tangent,
                slip_plane_constraints=constraints,
            ),
            scenario_index=scenario_index,
            calculation_index=calculation_index,
        )

    def serialize(self, filename: str):
        self.model.serialize(Path(filename))

    @property
    def soil_dict(self) -> Dict:
        result = {}
        for soil in self.model.soils.Soils:
            result[soil.Code] = {
                "code": soil.Code,
                "name": soil.Name,
                "id": soil.Id,
                "yd": soil.VolumetricWeightAbovePhreaticLevel,
                "ys": soil.VolumetricWeightBelowPhreaticLevel,
            }
        return result

    def layerid_soilid_dict(
        self, scenario_index: int = 0, stage_index: int = 0
    ) -> Dict:
        result = {}
        for sl in self.model.datastructure._get_soil_layers(
            scenario_index, stage_index
        ).SoilLayers:
            result[sl.LayerId] = sl.SoilId
        return result

    def layer_dict(self, scenario_index: int = 0, stage_index: int = 0) -> Dict:
        result = {}

        # create a dictionary with the soil id as key and the soil as value
        soilid_dict = {v["id"]: v for _, v in self.soil_dict.items()}

        # get the layer soil connection key = layer_id value = soil_id
        layerid_soilid_dict = self.layerid_soilid_dict(scenario_index, stage_index)

        for layer in self.model._get_geometry(scenario_index, stage_index).Layers:
            result[layer.Id] = {
                "points": [(float(p.X), float(p.Z)) for p in layer.Points],
                "soil": soilid_dict[layerid_soilid_dict[layer.Id]],
            }

        return result

    def soillayer_at(
        self, x: float, z: float, scenario_index: int = 0, stage_index: int = 0
    ) -> Optional[Dict]:
        for id, layer in self.layer_dict(scenario_index, stage_index).items():
            # check if the point is in the polygon of the layer
            if is_point_in_or_on_polygon((x, z), layer["points"]):
                return layer

        return None

    def default_consolidation_dict(
        self,
        max_soilweight: float = 16.0,
        scenario_index: int = 0,
        stage_index: int = 0,
        default_consolidation: float = DEFAULT_LOAD_CONSOLIDATION,
    ) -> Dict:
        result = {}
        for layer_id, layer in self.layer_dict(scenario_index, stage_index).items():
            if layer["soil"]["ys"] < max_soilweight:
                result[layer_id] = default_consolidation
            else:
                result[layer_id] = 100.0
        return result

    def add_traffic_load(
        self,
        label: str,
        start: float,
        width: float,
        magnitude: float,
        spread: float = DEFAULT_LOAD_SPREAD,
        scenario_index: int = 0,
        stage_index: int = 0,
    ):
        consolidation_dict = self.default_consolidation_dict()
        self.model.add_load(
            UniformLoad(
                label=label,
                start=start,
                end=start + width,
                magnitude=magnitude,
                angle_of_distribution=spread,
            ),
            consolidations=[
                Consolidation(degree=degree, layer_id=layer_id)
                for layer_id, degree in consolidation_dict.items()
            ],
            scenario_index=scenario_index,
            stage_index=stage_index,
        )

    def move_traffic_load(
        self, start: float, scenario_index: int = 0, stage_index: int = 0
    ):
        loads = self.model._get_loads(scenario_index, stage_index)

        if len(loads.UniformLoads) == 1:
            width = loads.UniformLoads[0].End - loads.UniformLoads[0].Start
            loads.UniformLoads[0].Start = start
            loads.UniformLoads[0].End = start + width
        else:
            raise ValueError(f"No or more than one load found in stage {stage_index}")

    def add_bbf_slipplane_constraints(
        self,
        min_slipplane_length: float = 0.0,
        min_slipplane_depth: float = 0.0,
        scenario_index: int = 0,
        calculation_index: int = 0,
    ):
        # something to do?
        add_constraints = min_slipplane_length > 0.0 or min_slipplane_depth > 0.0

        # check if we have the correct analysis type
        analysis_type = self.analysis_type(scenario_index, calculation_index)
        if analysis_type != AnalysisTypeEnum.BISHOP_BRUTE_FORCE:
            raise ValueError(
                f"Trying to add constraints to a '{analysis_type}' calculation, this only works for Bishop Brute Force calculation"
            )

        cs = self.model._get_calculation_settings(scenario_index, calculation_index)

        if add_constraints:
            self.set_bbf(
                left=cs.BishopBruteForce.SearchGrid.BottomLeft.X,
                bottom=cs.BishopBruteForce.SearchGrid.BottomLeft.Z,
                space=cs.BishopBruteForce.SearchGrid.Space,
                numx=cs.BishopBruteForce.SearchGrid.NumberOfPointsInX,
                numz=cs.BishopBruteForce.SearchGrid.NumberOfPointsInZ,
                bottom_tangent=cs.BishopBruteForce.TangentLines.BottomTangentLineZ,
                space_tangent=cs.BishopBruteForce.TangentLines.Space,
                numt=cs.BishopBruteForce.TangentLines.NumberOfTangentLines,
                scenario_index=scenario_index,
                calculation_index=calculation_index,
                add_constraints=True,
                min_slipplane_length=min_slipplane_length,
                min_slipplane_depth=min_slipplane_depth,
            )

    def get_waternet_creator_settings(
        self, scenario_index: int = 0, stage_index: int = 0
    ) -> WaternetCreatorSettings:
        wnet_settings_id = (
            self.model.datastructure.scenarios[scenario_index]
            .Stages[stage_index]
            .WaternetCreatorSettingsId
        )

        for wnet_setting in self.model.datastructure.waternetcreatorsettings:
            if wnet_setting.Id == wnet_settings_id:
                return wnet_setting

        raise ValueError(
            f"No waternet creator settings found for stage {stage_index} in scenario {scenario_index}."
        )

    def _generate_soilpolygons(self, scenario_index: int = 0, stage_index: int = 0):
        pass

    def change_limits(
        self,
        left: float = None,
        right: float = None,
        scenario_index: int = 0,
        stage_index: int = 0,
    ):
        # TODO what about the pl lines?
        old_left = self.left(scenario_index, stage_index)
        old_right = self.right(scenario_index, stage_index)

        if left is not None and old_left < left:
            raise ValueError("Cannot decrease the limits")
        if right is not None and old_right > right:
            raise ValueError("Cannot decrease the limits")

        # change it for all stages in the scenario
        for i in range(len(self.model.datastructure.scenarios[scenario_index].Stages)):
            geometry = self.model._get_geometry(scenario_index, i)
            for layer in geometry.Layers:
                for point in layer.Points:
                    if left is not None and point.X == old_left:
                        point.X = left
                    if right is not None and point.X == old_right:
                        point.X = right

    def get_surface_intersections(
        self,
        line: List[Tuple[float, float]],
        scenario_index: int = 0,
        stage_index: int = 0,
    ) -> List[Tuple[float, float]]:
        """Get the intersections of a line with the surface

        Args:
            line (List[Tuple[float, float]]): The line to check

        Returns:
            List[Tuple[float, float]]: The intersections of the line with the surface
        """
        return polyline_polyline_intersections(
            line, self.surface(scenario_index, stage_index)
        )

    def cut(
        self,
        line: List[Tuple[float, float]],
        scenario_index: int = 0,
        stage_index: int = 0,
    ):
        """Cut the model with a line defined by the points

        Args:
            line (List[Tuple[float, float]]): The points of the line
        """
        # change the last point to connect to the end of the surface
        # convert to list
        surface = self.surface(scenario_index, stage_index)
        intersections = polyline_polyline_intersections(line, surface)
        if len(intersections) == 0:
            return

        if len(intersections) % 2 == 1:
            dx = line[-1][0] - line[-2][0]
            dz = line[-1][1] - line[-2][1]
            x1 = intersections[-1][0]
            x2 = surface[-1][0]
            z1 = intersections[-1][1]
            z2 = z1 + (x2 - x1) / dx * dz
            intersections.append((x2, z2))

        for i in range(0, len(intersections), 2):
            start = intersections[i]
            end = intersections[i + 1]

            z1 = self.z_at(start[0], scenario_index, stage_index)
            p1 = Point(x=start[0], z=z1)

            if i == len(intersections) / 2:
                p2 = Point(x=end[0] - 0.01, z=end[1])
                p3 = Point(x=surface[-1][0], z=surface[-1][1])
                points = [p1, p2, p3]
            else:
                z2 = self.z_at(end[0], scenario_index, stage_index)
                p2 = Point(x=end[0], z=z2)
                points = [p1, p2]

            self.model.add_excavation(
                points=points,
                scenario_index=scenario_index,
                stage_index=stage_index,
                label="ontgraving",
            )

    def fill(
        self,
        line: List[Tuple[float, float]],
        soil_code: str,
        scenario_index: int = 0,
        stage_index: int = 0,
    ):
        """Fill the model with a line defined by the points

        Args:
            points (List[Tuple[float, float]]): The points of the line
            soil_code (str): The soil code to use for the fill
        """
        surface = self.surface(scenario_index, stage_index)
        intersections = polyline_polyline_intersections(line, surface)
        if len(intersections) == 0:
            return

        i = 1

    def _get_elevations(self, scenario_index: int, stage_index: int):
        decorations_id = (
            self.model.datastructure.scenarios[scenario_index]
            .Stages[stage_index]
            .DecorationsId
        )

        for decoration in self.decorations:
            if decoration.Id == decorations_id:
                return decoration.Elevations

        raise ValueError(
            f"No elevations found for stage {stage_index} in scenario {scenario_index}."
        )

    def add_elevation(
        self,
        points: List[Tuple[float, float]],
        label: str,
        scenario_index: int = 0,
        stage_index: int = 0,
    ):
        """Add an elevation to the model with a line defined by the points

        Args:
            points (List[Tuple[float, float]]): The points of the line
            soil_code (str): The soil code to use for the fill
        """
        persistable_elevation = PersistableElevation(
            Label=label,
            Points=[PersistablePoint(X=p.x, Z=p.z) for p in points],
        )
        self._get_elevations(scenario_index, stage_index).append(persistable_elevation)
