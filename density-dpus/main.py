from flask_api import status, FlaskAPI

app = FlaskAPI(__name__)

# TODO: replace # with """ for pydoc


@app.route('/counts/api/v1.0/active', methods=['POST'])
def record_movement(dpu_id: str, direction: int, timestamp: str):
    # args expected: dpu_id, direction (+/- 1), timestamp

    # this method impl will do the following:
    # query the k-v store for dpu_id -> (space_positive, space_negative, location_id).
    # 'space_positive' is the id of the space whose count should be incremented upon receiving a +1.
    # 'space_negative' is the id of the space whose count should be decremented upon receiving a +1.

    # (note that either of space_positive or space_negative could be null (but at least one should be non-null, or
    # it probably indicates some misconfiguration in the DB). The k-v store is expected to be initialized and kept
    # up to date with the metadata DB once it's been brought up so that it has this mapping available at all times.)

    # write to a queue a tuple of the form:
    # (space_positive, space_pos_count, space_negative, space_neg_count, timestamp)

    # if direction is +1, the tuple will be:
    #    (space_positive, +1, space_negative, -1, location_id)
    # else if direction is -1:
    #    (space_positive, -1, space_negative, +1, location_id)

    # also update the counts for the 'space_positive' and 'space_negative' spaces in the k-v store.

    # note that the k-v store will give approximate counts (potentially dipping into negative? if messages
    # arrive significantly out of order), whereas the historical counts should be more accurate since we try to actually
    # re-order the messages to more accurately reflect the real order in which the events occurred, before storing
    # to the backend timeseries DB.

    return ""


@app.route('/counts/api/v1.0/current/<string:space_id>', methods=['GET'])
def get_current_count(space_id: str):
    # args expected in request: the space_id.
    # returns the current known count for the specified space_id by querying the k-v store for the given
    # space_id.
    print(f'Getting the current count at space: {space_id}')
    return "0"


@app.route('/counts/api/v1.0/historical/<string:space_id>', methods=['GET'])
def get_historical_count(space_id: str, timestamp: str):
    # args expected in request: the space_id and timestamp.
    # queries the backend (such as timescale DB) and tries to get the
    # count as of the timestamp or nearest available timestamp.
    # the response includes the count as well as the timestamp closest to the specificed timestamp.
    print(f'Getting the historical count at space: {space_id}')
    return "0"


# Endpoints from here on are for managing the metadata which doesn't change as often,
# such as: locations, spaces, doorways, DPUs, etc. They are all prefixed with /metadata/.
# These endpoints could be used when setting up a DPU somewhere out in the field at a new location perhaps.

@app.route('/metadata/api/v1.0/locations/new', methods=['POST'])
def create_location():
    # args expected: as those of the logicical data model (ie, name, address etc).
    # creates a new location and returns the location id, enters the new location into the backend
    # database.
    print('Creating a new location')
    return ""


@app.route('/metadata/api/v1.0/locations/all', methods=['GET'])
def get_locations():
    # returns a list of all location IDs by querying the backend database.
    print('Returning all locations')
    return []


@app.route('/metadata/api/v1.0/locations/<string:location_id>/spaces/new', methods=['POST'])
def create_space(location_id: str):
    # args expected: details for the new space being added (as per the data model)
    # and the location id it's being added to.
    # returns the id for the new space by adding it to the backend database.
    print(f'Creating a new space at location {location_id}')
    return ""


@app.route('/metadata/api/v1.0/locations/<string:location_id>/spaces', methods=['GET'])
def get_spaces(location_id: str):
    # returns a list of all known spaces for the location by querying the backend database.
    print(f'Returning the spaces at location {location_id}')
    return []

# ... similar methods to create doorways and attach/detach DPUs


if __name__ == '__main__':
    # Note: switch off debug mode when in production
    app.run(debug=True)
