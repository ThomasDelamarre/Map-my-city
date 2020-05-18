import csv
import gpxpy


def createCsvFromEdges(edges, name):
    # Todo add .csv here and not when the ft is called
    with open("graphs_in_csv/" + name, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['From', "To", "distance", "required"])
        for edge in edges.edges:
            spamwriter.writerow([edge.node1.id, edge.node2.id, edge.length, edge.required])


def createCsvFromCircuit(circuit, name):
    with open("solutions_in_csv/" + name + ".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['From', "To", "Distance"])
        for line in circuit:
            spamwriter.writerow([line[0], line[1], line[3]["distance"]])


def readSolutionFromCsv(name):
    solution = []
    with open("solutions_in_csv/" + name + ".csv") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                if row[0] != "From" or row[1] != "To" or row[2] != "Distance":
                    raise TypeError("Solution file is not formated as expected")
                line_count += 1
            else:
                solution.append((row[0], row[1], row[2]))
    return solution




def createGpxFromCircuit(circuits, name):
    gpx_file = gpxpy.gpx.GPX()

    if isinstance(circuits, list):
        for circuit in circuits:
            # Create track in our GPX:
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx_file.tracks.append(gpx_track)

            # Create first segment in our GPX track:
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)

            # Create points:
            for edge in circuit.edges:
                addPointsFromEdge(edge, gpx_segment)

            gpx_lines = gpx_file.to_xml().splitlines()
    else:
        # Create track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_file.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        # Create points:
        for edge in circuits.edges:
            addPointsFromEdge(edge, gpx_segment)

        gpx_lines = gpx_file.to_xml().splitlines()

    file = open("gpx_files/" + name + ".gpx", 'w')
    for line in gpx_lines:
        file.write(line)
        file.write("\n")
    file.close()


def addPointsFromEdge(edge, gpx_segment):
    lats = edge.path.lats
    longs = edge.path.longs
    for i in range(edge.path.len):
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(longs[i], lats[i]))