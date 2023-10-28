from typing import Optional, List


def getEvents(eventNames: List[str], abi: Optional[list] = []):
    allEvents = []

    if not len(eventNames):
        return []

    for item in abi:
        eventsDict = {}

        if item['type'] == 'event' and not item['anonymous']:
            if len(eventNames) and item['name'] in eventNames:
                eventsDict['event'] = item['name']
                eventsDict['inputs'] = item['inputs']
                allEvents.append(eventsDict)

    return allEvents
