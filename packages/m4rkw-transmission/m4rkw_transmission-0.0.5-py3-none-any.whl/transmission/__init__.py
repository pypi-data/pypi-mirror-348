import requests
import json
import urllib
import re
import time

RPC_VERSION = 15
STATUSES = {
  0: 'stopped',
  1: 'check-wait',
  2: 'checking',
  3: 'download-wait',
  4: 'downloading',
  5: 'seed-wait',
  6: 'seeding'
}
RPC_METHODS = {
  'start':  'torrent-start',
  'stop':  'torrent-stop',
  'verify':  'torrent-verify',
  'reannounce':  'torrent-reannounce',
  'queue_top':  'queue-move-top',
  'queue_up':  'queue-move-up',
  'queue_down':  'queue-move-down',
  'queue_bottom':  'queue-move-bottom'
}

class Transmission:
#  attr_accessor :list_attributes
#  attr_accessor :settable_attributes

  def __init__(self, config):
    self.config = config

    self.list_attributes = ['id','name','hashString','isFinished','isStalled','leftUntilDone','eta','percentDone','rateDownload',
      'status','totalSize','rateDownload','peersConnected','peersFrom','rateUpload','downloadedEver','peersSendingToUs',
      'peersGettingFromUs','desiredAvailable']
    self.all_attributes = ['activityDate','addedDate','bandwidthPriority','comment','corruptEver','creator','dateCreated',
      'desiredAvailable','doneDate','downloadDir','downloadedEver','downloadLimit','downloadLimited','error',
      'errorString','eta','etaIdle','files','fileStats','hashString','haveUnchecked','haveValid','honorsSessionLimits',
      'id','isFinished','isPrivate','isStalled','leftUntilDone','magnetLink','manualAnnounceTime','maxConnectedPeers',
      'metadataPercentComplete','name','peer-limit','peers','peersConnected','peersFrom','peersGettingFromUs',
      'peersSendingToUs','percentDone','pieces','pieceCount','pieceSize','priorities','queuePosition','rateDownload',
      'rateUpload','recheckProgress','secondsDownloading','secondsSeeding','seedIdleLimit','seedIdleMode','seedRatioLimit',
      'seedRatioMode','sizeWhenDone','startDate','status','trackers','trackerStats','totalSize','torrentFile',
      'uploadedEver','uploadLimit','uploadLimited','uploadRatio','wanted','webseeds','webseedsSendingToUs','files-wanted','files-unwanted']
    self.settable_attributes = ['bandwidthPriority','downloadLimit','downloadLimited','files-wanted','files-unwanted',
      'honorsSessionLimits','location','peer-limit','priority-high','priority-low','priority-normal','queuePosition',
      'seedIdleLimit','seedIdleMode','seedRatioLimit','seedRatioMode','trackerAdd','trackerRemove','trackerReplace',
      'uploadLimit','uploadLimited']
    self.session_attributes = ['alt-speed-down','alt-speed-enabled','alt-speed-time-begin','alt-speed-time-enabled',
      'alt-speed-time-end','alt-speed-time-day','alt-speed-up','blocklist-url','blocklist-enabled','blocklist-size',
      'cache-size-mb','config-dir','download-dir','download-queue-size','download-queue-enabled','dht-enabled',
      'encryption','idle-seeding-limit','idle-seeding-limit-enabled','incomplete-dir','incomplete-dir-enabled',
      'lpd-enabled','peer-limit-global','peer-limit-per-torrent','pex-enabled','peer-port','peer-port-random-on-start',
      'port-forwarding-enabled','queue-stalled-enabled','queue-stalled-minutes','rename-partial-files','rpc-version',
      'rpc-version-minimum','script-torrent-done-filename','script-torrent-done-enabled','seedRatioLimit','seedRatioLimited',
      'seed-queue-size','seed-queue-enabled','speed-limit-down','speed-limit-down-enabled','speed-limit-up',
      'speed-limit-up-enabled','start-added-torrents','trash-original-torrent-files','units','utp-enabled','version','units']
    self.session_settable_attributes = ['alt-speed-down','alt-speed-enabled','alt-speed-time-begin','alt-speed-time-enabled',
      'alt-speed-time-end','alt-speed-time-day','alt-speed-up','blocklist-url','blocklist-enabled','cache-size-mb',
      'download-dir','download-queue-size','download-queue-enabled','dht-enabled','encryption','idle-seeding-limit',
      'idle-seeding-limit-enabled','incomplete-dir','incomplete-dir-enabled','lpd-enabled','peer-limit-global',
      'peer-limit-per-torrent','pex-enabled','peer-port','peer-port-random-on-start','port-forwarding-enabled',
      'queue-stalled-enabled','queue-stalled-minutes','rename-partial-files','script-torrent-done-filename',
      'script-torrent-done-enabled','seedRatioLimit','seedRatioLimited','seed-queue-size','seed-queue-enabled',
      'speed-limit-down','speed-limit-down-enabled','speed-limit-up','speed-limit-up-enabled','start-added-torrents',
      'trash-original-torrent-files','units','utp-enabled','units']

#    rpc_version = self.session_get()['rpc-version']
#
#    if rpc_version != RPC_VERSION:
#      print("--------------------------------------------------------")
#      print("WARNING: RPC version is #{rpc_version} but we only support #{$rpc_version}.")
#      print("Some API methods may fail or produce unexpected results.")
#      print("Please check for an update to this gem.")
#      print("--------------------------------------------------------")


  def rpc(self, method, args=[], session_id=None):
    resp = None

    resp = requests.post('http://%s:%d/transmission/rpc' % (self.config['host'], self.config['port']), json={
        'method': method,
        'arguments': args
      }, headers={
        'X-Transmission-Session-Id': session_id,
        'Content-type': 'application/json'
      }, auth=(self.config['user'], self.config['pass']))

    if resp.status_code == 409:
      match = re.match('^.*?X-Transmission-Session-Id: (.*?)<', resp.text)

      return self.rpc(method, args, match.group(1))

    response = json.loads(resp.text)

    if response["result"] != "success":
      raise Exception("RPC error: " + response["result"])

    return response


  def get(self, ids=[], attributes=[]):
    for attr in attributes:
      if attr not in self.all_attributes:
        raise Exception("Unknown torrent attributes: %s" % (attr))

    if len(attributes) == 0:
      attributes = self.all_attributes

    params = {
      'fields': attributes
    }

    if isinstance(ids, int):
      ids = [ids]
      single = True
    else:
      single = False

    if len(ids) >0:
      params['ids'] = ids

    resp = self.rpc('torrent-get', params)

    for i in range(0, len(resp["arguments"]["torrents"])):
      for key in resp["arguments"]["torrents"][i]:
        method_s = 'map_%s' % (key)

        try:
          method = getattr(self, method_s)
          resp["arguments"]["torrents"][i][key] = method(resp["arguments"]["torrents"][i][key])
        except:
          pass

    if single:
      if len(resp["arguments"]["torrents"]) >0:
        return resp["arguments"]["torrents"][0]

      return False

    return resp["arguments"]["torrents"]


  def list(self):
    return self.get([], self.list_attributes)


  def list_by(self, field, operator, value=None):
    torrents = []

    if value == None:
      value = operator
      operator = '='

    for torrent in self.list():
      if self.eval_operator(torrent[field], operator, value):
          torrents.append(torrent)

    return torrents


  def eval_operator(self, torrent_value, operator, value):
    if operator in ['=','==']:
      return torrent_value == value
    if operator == '>':
      return torrent_value > value
    if operator == '<':
      return torrent_value < value
    if operator == '>=':
      return torrent_value >= value
    if operator == '<=':
      return torrent_value <= value
    if operator in ['!=','<>']:
      return torrent_value != value

    raise Exception("Unknown comparison operator: %s" % (operator))


  def map_name(self, name):
    return urllib.unquote(name).replace('+',' ')


  def map_status(self, code):
    if code in STATUSES:
      return STATUSES[code]

    raise Exception("Unknown status code: %s" % (code))


  def map_percentDone(self, percent):
    return percent * 100


  def get_attr(self, _id, attribute):
    resp = self.get([_id], [attribute])

    return resp[0][attribute]


  def set_attr(self, _id, attribute, value):
    resp = self.rpc('torrent-set', {'ids': [_id], attribute: value})

    return resp


  def get_attrs(self, ids, attributes):
    return self.get(ids, attributes)


  def add(self, params={}):
    resp = self.rpc('torrent-add', params)

    if 'torrent-added' in resp['arguments']:
      return resp["arguments"]["torrent-added"]

    return False


  def all_ids(self):
    ids = []

    for tor in self.list():
      ids.append(tor['id'])

    return ids


  def add_magnet(self, magnet_link, params={}):
    if magnet_link[0:8] != 'magnet:?':
      raise Exception("This doesn't look like a magnet link to me: %s" % (magnet_link))

    ids_before = self.all_ids()

    arg = {'filename': magnet_link}

    if params:
        arg.update(params)

    self.add(arg)

    while 1:
      for _id in self.all_ids():
        if _id not in ids_before:
          return _id

      time.sleep(0.1)


  def add_torrentfile(self, torrent_file, params={}):
    self.add({'filename': torrent_file}.update(params))


  def add_torrentdata(self, torrent_data, params={}):
    self.add({'metainfo': torrent_data}.update(params))


  def __getattr__(self, attr):
    if attr in RPC_METHODS:
      def execute_rpc_method(*args, **kwargs):
        return self.rpc(RPC_METHODS[attr], kwargs)

      return execute_rpc_method

    raise Exception("method missing: %s" % (attr))


  def set(self, ids, keys):
    for key in keys:
      if key not in self.settable_attributes:
        raise Exception("Unknown attribute: %s" % (key))

    return self.rpc('torrent-set',{
        'ids': ids
      }.update(keys))


  def delete(self, ids, delete_local_data=False):
    return self.rpc('torrent-remove',{
      'ids': ids,
      'delete-local-data': delete_local_data
    })


  def set_location(self, ids, location, move=False):
    return self.rpc('torrent-set-location',{
      'ids': ids,
      'location': location,
      'move': move
    })


  def rename_path(self, ids, path, name):
    return self.rpc('torrent-rename-path',{
      'ids': ids,
      'path': path,
      'name': name
    })


  def session_get(self):
    resp = self.rpc('session-get')

    return resp['arguments']


  def session_set(self, keys):
    for key in keys:
      if key not in session_attributes:
        raise Exception("Unknown session attribute: %s" % (key))

      if key not in session_settable_attributes:
        raise Exception("Session attribute '%s' cannot be changed." % (key))

    return self.rpc('session-set', keys)


  def session_stats(self):
    resp = self.rpc('session-stats')

    return resp['arguments']


  def blocklist_update(self):
    resp = self.rpc('blocklist-update')

    return resp['arguments']


  def port_test(self):
    resp = self.rpc('port-test')

    return resp['arguments']['port-is-open']


  def session_close(self):
    return self.rpc('session-close')


  def free_space(self, path):
    resp = self.rpc('free-space',{'path': path})

    return resp['arguments']
